import os
import shutil
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, List, Literal, Optional, Sequence, Union
import click
import pandas as pd
from colorama import Fore, Style
from pydantic import Field, StrictStr
from pytz import utc
from tqdm import tqdm
import feast
from feast.batch_feature_view import BatchFeatureView
from feast.entity import Entity
from feast.feature_view import FeatureView
from feast.infra.materialization.batch_materialization_engine import BatchMaterializationEngine, MaterializationJob, MaterializationJobStatus, MaterializationTask
from feast.infra.offline_stores.offline_store import OfflineStore
from feast.infra.online_stores.online_store import OnlineStore
from feast.infra.registry.base_registry import BaseRegistry
from feast.infra.utils.snowflake.snowflake_utils import _run_snowflake_field_mapping, assert_snowflake_feature_names, execute_snowflake_statement, get_snowflake_conn, get_snowflake_online_store_path, package_snowpark_zip
from feast.protos.feast.types.EntityKey_pb2 import EntityKey as EntityKeyProto
from feast.protos.feast.types.Value_pb2 import Value as ValueProto
from feast.repo_config import FeastConfigBaseModel, RepoConfig
from feast.stream_feature_view import StreamFeatureView
from feast.type_map import _convert_value_name_to_snowflake_udf
from feast.utils import _coerce_datetime, _get_column_names


def _materialize_one(self, registry: BaseRegistry, feature_view: Union[(BatchFeatureView, StreamFeatureView, FeatureView)], start_date: datetime, end_date: datetime, project: str, tqdm_builder: Callable[([int], tqdm)]):
    assert (isinstance(feature_view, BatchFeatureView) or isinstance(feature_view, FeatureView)), 'Snowflake can only materialize FeatureView & BatchFeatureView feature view types.'
    entities = []
    for entity_name in feature_view.entities:
        entities.append(registry.get_entity(entity_name, project))
    (join_key_columns, feature_name_columns, timestamp_field, created_timestamp_column) = _get_column_names(feature_view, entities)
    job_id = f'{feature_view.name}-{start_date}-{end_date}'
    try:
        offline_job = self.offline_store.pull_latest_from_table_or_query(config=self.repo_config, data_source=feature_view.batch_source, join_key_columns=join_key_columns, feature_name_columns=feature_name_columns, timestamp_field=timestamp_field, created_timestamp_column=created_timestamp_column, start_date=start_date, end_date=end_date)
        with get_snowflake_conn(self.repo_config.offline_store) as conn:
            query = f"SELECT SYSTEM$LAST_CHANGE_COMMIT_TIME('{feature_view.batch_source.get_table_query_string()}') AS last_commit_change_time"
            last_commit_change_time = (conn.cursor().execute(query).fetchall()[0][0] / 1000000000)
        if (last_commit_change_time < start_date.astimezone(tz=utc).timestamp()):
            return SnowflakeMaterializationJob(job_id=job_id, status=MaterializationJobStatus.SUCCEEDED)
        fv_latest_values_sql = offline_job.to_sql()
        if (feature_view.batch_source.field_mapping is not None):
            fv_latest_mapped_values_sql = _run_snowflake_field_mapping(fv_latest_values_sql, feature_view.batch_source.field_mapping)
        fv_to_proto_sql = self.generate_snowflake_materialization_query(self.repo_config, fv_latest_mapped_values_sql, feature_view, project)
        if (self.repo_config.online_store.type == 'snowflake.online'):
            self.materialize_to_snowflake_online_store(self.repo_config, fv_to_proto_sql, feature_view, project)
        else:
            self.materialize_to_external_online_store(self.repo_config, fv_to_proto_sql, feature_view, tqdm_builder)
        return SnowflakeMaterializationJob(job_id=job_id, status=MaterializationJobStatus.SUCCEEDED)
    except BaseException as e:
        return SnowflakeMaterializationJob(job_id=job_id, status=MaterializationJobStatus.ERROR, error=e)
