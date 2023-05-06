import warnings
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union
import numpy as np
import pandas
import pyarrow
import pyarrow as pa
import sqlalchemy
from pydantic.types import StrictStr
from pydantic.typing import Literal
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from feast import FileSource, errors
from feast.data_source import DataSource
from feast.errors import InvalidEntityType
from feast.feature_logging import LoggingConfig, LoggingSource
from feast.feature_view import FeatureView
from feast.infra.offline_stores import offline_utils
from feast.infra.offline_stores.file_source import SavedDatasetFileStorage
from feast.infra.offline_stores.offline_store import OfflineStore, RetrievalMetadata
from feast.infra.offline_stores.offline_utils import DEFAULT_ENTITY_DF_EVENT_TIMESTAMP_COL, build_point_in_time_query, get_feature_view_query_context
from feast.infra.provider import RetrievalJob
from feast.infra.registry.base_registry import BaseRegistry
from feast.on_demand_feature_view import OnDemandFeatureView
from feast.repo_config import FeastBaseModel, RepoConfig
from feast.saved_dataset import SavedDatasetStorage
from feast.type_map import pa_to_mssql_type
from feast.usage import log_exceptions_and_usage


@staticmethod
@log_exceptions_and_usage(offline_store='mssql')
def pull_all_from_table_or_query(config: RepoConfig, data_source: DataSource, join_key_columns: List[str], feature_name_columns: List[str], timestamp_field: str, start_date: datetime, end_date: datetime) -> RetrievalJob:
    assert (type(data_source).__name__ == 'MsSqlServerSource')
    warnings.warn('The Azure Synapse + Azure SQL offline store is an experimental feature in alpha development. Some functionality may still be unstable so functionality can change in the future.', RuntimeWarning)
    from_expression = data_source.get_table_query_string().replace('`', '')
    timestamps = [timestamp_field]
    field_string = ', '.join(((join_key_columns + feature_name_columns) + timestamps))
    query = f'''
            SELECT {field_string}
            FROM (
                SELECT {field_string}
                FROM {from_expression}
                WHERE {timestamp_field} BETWEEN TIMESTAMP '{start_date}' AND TIMESTAMP '{end_date}'
            )
            '''
    engine = make_engine(config.offline_store)
    return MsSqlServerRetrievalJob(query=query, engine=engine, config=config.offline_store, full_feature_names=False, on_demand_feature_views=None)