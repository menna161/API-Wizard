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


def materialize_to_external_online_store(self, repo_config: RepoConfig, materialization_sql: str, feature_view: Union[(StreamFeatureView, FeatureView)], tqdm_builder: Callable[([int], tqdm)]) -> None:
    feature_names = [feature.name for feature in feature_view.features]
    with get_snowflake_conn(repo_config.batch_engine) as conn:
        query = materialization_sql
        cursor = execute_snowflake_statement(conn, query)
        for (i, df) in enumerate(cursor.fetch_pandas_batches()):
            click.echo(f'Snowflake: Processing Materialization ResultSet Batch #{(i + 1)}')
            entity_keys = df['entity_key'].apply(EntityKeyProto.FromString).to_numpy()
            for feature in feature_names:
                df[feature] = df[feature].apply(ValueProto.FromString)
            features = df[feature_names].to_dict('records')
            event_timestamps = [_coerce_datetime(val) for val in pd.to_datetime(df[feature_view.batch_source.timestamp_field])]
            if feature_view.batch_source.created_timestamp_column:
                created_timestamps = [_coerce_datetime(val) for val in pd.to_datetime(df[feature_view.batch_source.created_timestamp_column])]
            else:
                created_timestamps = ([None] * df.shape[0])
            rows_to_write = list(zip(entity_keys, features, event_timestamps, created_timestamps))
            with tqdm_builder(len(rows_to_write)) as pbar:
                self.online_store.online_write_batch(repo_config, feature_view, rows_to_write, (lambda x: pbar.update(x)))
    return None
