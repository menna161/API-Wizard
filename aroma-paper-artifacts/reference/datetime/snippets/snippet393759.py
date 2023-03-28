import warnings
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, List, Optional, Union
import pandas as pd
import pyarrow
from feast import flags_helper
from feast.data_source import DataSource
from feast.dqm.errors import ValidationFailed
from feast.feature_logging import LoggingConfig, LoggingSource
from feast.feature_view import FeatureView
from feast.infra.registry.base_registry import BaseRegistry
from feast.on_demand_feature_view import OnDemandFeatureView
from feast.repo_config import RepoConfig
from feast.saved_dataset import SavedDatasetStorage
from feast.saved_dataset import ValidationReference


def __init__(self, features: List[str], keys: List[str], min_event_timestamp: Optional[datetime]=None, max_event_timestamp: Optional[datetime]=None):
    self.features = features
    self.keys = keys
    self.min_event_timestamp = min_event_timestamp
    self.max_event_timestamp = max_event_timestamp
