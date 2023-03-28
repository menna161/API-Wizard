from dataclasses import dataclass
from datetime import datetime
from typing import Callable, List, Literal, Optional, Sequence, Union, cast
import dill
import pandas as pd
import pyarrow
from tqdm import tqdm
from feast.batch_feature_view import BatchFeatureView
from feast.entity import Entity
from feast.feature_view import FeatureView
from feast.infra.materialization.batch_materialization_engine import BatchMaterializationEngine, MaterializationJob, MaterializationJobStatus, MaterializationTask
from feast.infra.offline_stores.contrib.spark_offline_store.spark import SparkOfflineStore, SparkRetrievalJob
from feast.infra.online_stores.online_store import OnlineStore
from feast.infra.passthrough_provider import PassthroughProvider
from feast.infra.registry.base_registry import BaseRegistry
from feast.protos.feast.core.FeatureView_pb2 import FeatureView as FeatureViewProto
from feast.repo_config import FeastConfigBaseModel, RepoConfig
from feast.stream_feature_view import StreamFeatureView
from feast.utils import _convert_arrow_to_proto, _get_column_names, _run_pyarrow_field_mapping


def _materialize_one(self, registry: BaseRegistry, feature_view: Union[(BatchFeatureView, StreamFeatureView, FeatureView)], start_date: datetime, end_date: datetime, project: str, tqdm_builder: Callable[([int], tqdm)]):
    entities = []
    for entity_name in feature_view.entities:
        entities.append(registry.get_entity(entity_name, project))
    (join_key_columns, feature_name_columns, timestamp_field, created_timestamp_column) = _get_column_names(feature_view, entities)
    job_id = f'{feature_view.name}-{start_date}-{end_date}'
    try:
        offline_job = cast(SparkRetrievalJob, self.offline_store.pull_latest_from_table_or_query(config=self.repo_config, data_source=feature_view.batch_source, join_key_columns=join_key_columns, feature_name_columns=feature_name_columns, timestamp_field=timestamp_field, created_timestamp_column=created_timestamp_column, start_date=start_date, end_date=end_date))
        spark_serialized_artifacts = _SparkSerializedArtifacts.serialize(feature_view=feature_view, repo_config=self.repo_config)
        spark_df = offline_job.to_spark_df()
        if (self.repo_config.batch_engine.partitions != 0):
            spark_df = spark_df.repartition(self.repo_config.batch_engine.partitions)
        spark_df.foreachPartition((lambda x: _process_by_partition(x, spark_serialized_artifacts)))
        return SparkMaterializationJob(job_id=job_id, status=MaterializationJobStatus.SUCCEEDED)
    except BaseException as e:
        return SparkMaterializationJob(job_id=job_id, status=MaterializationJobStatus.ERROR, error=e)
