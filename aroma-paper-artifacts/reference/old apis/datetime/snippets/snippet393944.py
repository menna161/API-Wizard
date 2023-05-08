from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
import pandas as pd
import pyarrow
from tqdm import tqdm
from feast import FeatureService, errors
from feast.entity import Entity
from feast.feature_view import FeatureView
from feast.importer import import_class
from feast.infra.infra_object import Infra
from feast.infra.offline_stores.offline_store import RetrievalJob
from feast.infra.registry.base_registry import BaseRegistry
from feast.protos.feast.core.Registry_pb2 import Registry as RegistryProto
from feast.protos.feast.types.EntityKey_pb2 import EntityKey as EntityKeyProto
from feast.protos.feast.types.Value_pb2 import Value as ValueProto
from feast.repo_config import RepoConfig
from feast.saved_dataset import SavedDataset


@abstractmethod
def materialize_single_feature_view(self, config: RepoConfig, feature_view: FeatureView, start_date: datetime, end_date: datetime, registry: BaseRegistry, project: str, tqdm_builder: Callable[([int], tqdm)]) -> None:
    '\n        Writes latest feature values in the specified time range to the online store.\n\n        Args:\n            config: The config for the current feature store.\n            feature_view: The feature view to materialize.\n            start_date: The start of the time range.\n            end_date: The end of the time range.\n            registry: The registry for the current feature store.\n            project: Feast project to which the objects belong.\n            tqdm_builder: A function to monitor the progress of materialization.\n        '
    pass
