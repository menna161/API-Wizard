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


@staticmethod
@abstractmethod
def pull_all_from_table_or_query(config: RepoConfig, data_source: DataSource, join_key_columns: List[str], feature_name_columns: List[str], timestamp_field: str, start_date: datetime, end_date: datetime) -> RetrievalJob:
    '\n        Extracts all the entity rows (i.e. the combination of join key columns, feature columns, and\n        timestamp columns) from the specified data source that lie within the specified time range.\n\n        All of the column names should refer to columns that exist in the data source. In particular,\n        any mapping of column names must have already happened.\n\n        Args:\n            config: The config for the current feature store.\n            data_source: The data source from which the entity rows will be extracted.\n            join_key_columns: The columns of the join keys.\n            feature_name_columns: The columns of the features.\n            timestamp_field: The timestamp column.\n            start_date: The start of the time range.\n            end_date: The end of the time range.\n\n        Returns:\n            A RetrievalJob that can be executed to get the entity rows.\n        '
    pass
