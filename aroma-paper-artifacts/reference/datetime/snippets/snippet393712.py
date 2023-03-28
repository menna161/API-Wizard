from dataclasses import dataclass
from datetime import datetime
from typing import Callable, List, Literal, Optional, Sequence, Union
from tqdm import tqdm
from feast.batch_feature_view import BatchFeatureView
from feast.entity import Entity
from feast.feature_view import FeatureView
from feast.infra.offline_stores.offline_store import OfflineStore
from feast.infra.online_stores.online_store import OnlineStore
from feast.infra.registry.base_registry import BaseRegistry
from feast.repo_config import FeastConfigBaseModel, RepoConfig
from feast.stream_feature_view import StreamFeatureView
from feast.utils import _convert_arrow_to_proto, _get_column_names, _run_pyarrow_field_mapping
from .batch_materialization_engine import BatchMaterializationEngine, MaterializationJob, MaterializationJobStatus, MaterializationTask


def _materialize_one(self, registry: BaseRegistry, feature_view: Union[(BatchFeatureView, StreamFeatureView, FeatureView)], start_date: datetime, end_date: datetime, project: str, tqdm_builder: Callable[([int], tqdm)]):
    entities = []
    for entity_name in feature_view.entities:
        entities.append(registry.get_entity(entity_name, project))
    (join_key_columns, feature_name_columns, timestamp_field, created_timestamp_column) = _get_column_names(feature_view, entities)
    job_id = f'{feature_view.name}-{start_date}-{end_date}'
    try:
        offline_job = self.offline_store.pull_latest_from_table_or_query(config=self.repo_config, data_source=feature_view.batch_source, join_key_columns=join_key_columns, feature_name_columns=feature_name_columns, timestamp_field=timestamp_field, created_timestamp_column=created_timestamp_column, start_date=start_date, end_date=end_date)
        table = offline_job.to_arrow()
        if (feature_view.batch_source.field_mapping is not None):
            table = _run_pyarrow_field_mapping(table, feature_view.batch_source.field_mapping)
        join_key_to_value_type = {entity.name: entity.dtype.to_value_type() for entity in feature_view.entity_columns}
        with tqdm_builder(table.num_rows) as pbar:
            for batch in table.to_batches(DEFAULT_BATCH_SIZE):
                rows_to_write = _convert_arrow_to_proto(batch, feature_view, join_key_to_value_type)
                self.online_store.online_write_batch(self.repo_config, feature_view, rows_to_write, (lambda x: pbar.update(x)))
        return LocalMaterializationJob(job_id=job_id, status=MaterializationJobStatus.SUCCEEDED)
    except BaseException as e:
        return LocalMaterializationJob(job_id=job_id, status=MaterializationJobStatus.ERROR, error=e)
