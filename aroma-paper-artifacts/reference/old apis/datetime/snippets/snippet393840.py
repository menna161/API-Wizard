from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import pandas as pd
import pyarrow as pa
from tqdm import tqdm
from feast import importer
from feast.batch_feature_view import BatchFeatureView
from feast.entity import Entity
from feast.feature_logging import FeatureServiceLoggingSource
from feast.feature_service import FeatureService
from feast.feature_view import FeatureView
from feast.infra.materialization.batch_materialization_engine import BatchMaterializationEngine, MaterializationJobStatus, MaterializationTask
from feast.infra.offline_stores.offline_store import RetrievalJob
from feast.infra.offline_stores.offline_utils import get_offline_store_from_config
from feast.infra.online_stores.helpers import get_online_store_from_config
from feast.infra.provider import Provider
from feast.infra.registry.base_registry import BaseRegistry
from feast.protos.feast.types.EntityKey_pb2 import EntityKey as EntityKeyProto
from feast.protos.feast.types.Value_pb2 import Value as ValueProto
from feast.repo_config import BATCH_ENGINE_CLASS_FOR_TYPE, RepoConfig
from feast.saved_dataset import SavedDataset
from feast.stream_feature_view import StreamFeatureView
from feast.usage import RatioSampler, log_exceptions_and_usage, set_usage_attribute
from feast.utils import _convert_arrow_to_proto, _run_pyarrow_field_mapping, make_tzaware


def materialize_single_feature_view(self, config: RepoConfig, feature_view: FeatureView, start_date: datetime, end_date: datetime, registry: BaseRegistry, project: str, tqdm_builder: Callable[([int], tqdm)]) -> None:
    set_usage_attribute('provider', self.__class__.__name__)
    assert (isinstance(feature_view, BatchFeatureView) or isinstance(feature_view, StreamFeatureView) or isinstance(feature_view, FeatureView)), f'Unexpected type for {feature_view.name}: {type(feature_view)}'
    task = MaterializationTask(project=project, feature_view=feature_view, start_time=start_date, end_time=end_date, tqdm_builder=tqdm_builder)
    jobs = self.batch_engine.materialize(registry, [task])
    assert (len(jobs) == 1)
    if ((jobs[0].status() == MaterializationJobStatus.ERROR) and jobs[0].error()):
        e = jobs[0].error()
        assert e
        raise e
