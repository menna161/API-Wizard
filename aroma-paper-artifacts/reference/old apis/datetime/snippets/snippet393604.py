from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import pandas
import pyarrow
from tqdm import tqdm
from feast import Entity, FeatureService, FeatureView, RepoConfig
from feast.infra.offline_stores.offline_store import RetrievalJob
from feast.infra.provider import Provider
from feast.infra.registry.base_registry import BaseRegistry
from feast.protos.feast.types.EntityKey_pb2 import EntityKey as EntityKeyProto
from feast.protos.feast.types.Value_pb2 import Value as ValueProto
from feast.saved_dataset import SavedDataset


def online_write_batch(self, config: RepoConfig, table: FeatureView, data: List[Tuple[(EntityKeyProto, Dict[(str, ValueProto)], datetime, Optional[datetime])]], progress: Optional[Callable[([int], Any)]]) -> None:
    pass
