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
def retrieve_feature_service_logs(self, feature_service: FeatureService, start_date: datetime, end_date: datetime, config: RepoConfig, registry: BaseRegistry) -> RetrievalJob:
    '\n        Reads logged features for the specified time window.\n\n        Args:\n            feature_service: The feature service whose logs should be retrieved.\n            start_date: The start of the window.\n            end_date: The end of the window.\n            config: The config for the current feature store.\n            registry: The registry for the current feature store.\n\n        Returns:\n            A RetrievalJob that can be executed to get the feature service logs.\n        '
    pass
