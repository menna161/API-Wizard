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


def online_write_batch(self, config: RepoConfig, table: FeatureView, data: List[Tuple[(EntityKeyProto, Dict[(str, ValueProto)], datetime, Optional[datetime])]], progress: Optional[Callable[([int], Any)]]) -> None:
    set_usage_attribute('provider', self.__class__.__name__)
    if self.online_store:
        self.online_store.online_write_batch(config, table, data, progress)
