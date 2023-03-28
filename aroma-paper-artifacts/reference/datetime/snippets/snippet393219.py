import uuid
from datetime import datetime
from typing import Callable, List, Literal, Sequence, Union
import yaml
from kubernetes import client
from kubernetes import config as k8s_config
from kubernetes import utils
from kubernetes.utils import FailToCreateError
from pydantic import StrictStr
from tqdm import tqdm
from feast import FeatureView, RepoConfig
from feast.batch_feature_view import BatchFeatureView
from feast.entity import Entity
from feast.infra.materialization.batch_materialization_engine import BatchMaterializationEngine, MaterializationJob, MaterializationTask
from feast.infra.offline_stores.offline_store import OfflineStore
from feast.infra.online_stores.online_store import OnlineStore
from feast.infra.registry.base_registry import BaseRegistry
from feast.repo_config import FeastConfigBaseModel
from feast.stream_feature_view import StreamFeatureView
from feast.utils import _get_column_names, get_default_yaml_file_path
from .bytewax_materialization_job import BytewaxMaterializationJob


def _materialize_one(self, registry: BaseRegistry, feature_view: Union[(BatchFeatureView, StreamFeatureView, FeatureView)], start_date: datetime, end_date: datetime, project: str, tqdm_builder: Callable[([int], tqdm)]):
    entities = []
    for entity_name in feature_view.entities:
        entities.append(registry.get_entity(entity_name, project))
    (join_key_columns, feature_name_columns, timestamp_field, created_timestamp_column) = _get_column_names(feature_view, entities)
    offline_job = self.offline_store.pull_latest_from_table_or_query(config=self.repo_config, data_source=feature_view.batch_source, join_key_columns=join_key_columns, feature_name_columns=feature_name_columns, timestamp_field=timestamp_field, created_timestamp_column=created_timestamp_column, start_date=start_date, end_date=end_date)
    paths = offline_job.to_remote_storage()
    job_id = str(uuid.uuid4())
    return self._create_kubernetes_job(job_id, paths, feature_view)
