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


def _infer_event_timestamp_from_sqlserver_schema(table_schema) -> str:
    if any(((schema_field['COLUMN_NAME'] == DEFAULT_ENTITY_DF_EVENT_TIMESTAMP_COL) for schema_field in table_schema)):
        return DEFAULT_ENTITY_DF_EVENT_TIMESTAMP_COL
    else:
        datetime_columns = list(filter((lambda schema_field: (schema_field['DATA_TYPE'] == 'DATETIMEOFFSET')), table_schema))
        if (len(datetime_columns) == 1):
            print(f"Using {datetime_columns[0]['COLUMN_NAME']} as the event timestamp. To specify a column explicitly, please name it {DEFAULT_ENTITY_DF_EVENT_TIMESTAMP_COL}.")
            return datetime_columns[0].name
        else:
            raise ValueError(f'Please provide an entity_df with a column named {DEFAULT_ENTITY_DF_EVENT_TIMESTAMP_COL} representing the time of events.')
