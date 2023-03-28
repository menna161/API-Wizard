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


def _get_entity_df_event_timestamp_range(entity_df: Union[(pandas.DataFrame, str)], entity_df_event_timestamp_col: str, engine: Engine) -> Tuple[(datetime, datetime)]:
    if isinstance(entity_df, pandas.DataFrame):
        entity_df_event_timestamp = entity_df.loc[:, entity_df_event_timestamp_col].infer_objects()
        if pandas.api.types.is_string_dtype(entity_df_event_timestamp):
            entity_df_event_timestamp = pandas.to_datetime(entity_df_event_timestamp, utc=True)
        entity_df_event_timestamp_range = (entity_df_event_timestamp.min().to_pydatetime(), entity_df_event_timestamp.max().to_pydatetime())
    elif isinstance(entity_df, str):
        df = pandas.read_sql(entity_df, con=engine).fillna(value=np.nan)
        entity_df_event_timestamp = df.loc[:, entity_df_event_timestamp_col].infer_objects()
        if pandas.api.types.is_string_dtype(entity_df_event_timestamp):
            entity_df_event_timestamp = pandas.to_datetime(entity_df_event_timestamp, utc=True)
        entity_df_event_timestamp_range = (entity_df_event_timestamp.min().to_pydatetime(), entity_df_event_timestamp.max().to_pydatetime())
    else:
        raise InvalidEntityType(type(entity_df))
    return entity_df_event_timestamp_range
