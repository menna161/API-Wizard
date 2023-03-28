import contextlib
from dataclasses import asdict
from datetime import datetime
from typing import Any, Callable, ContextManager, Dict, Iterator, KeysView, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
import pyarrow as pa
from jinja2 import BaseLoader, Environment
from psycopg2 import sql
from pydantic.typing import Literal
from pytz import utc
from feast.data_source import DataSource
from feast.errors import InvalidEntityType
from feast.feature_view import DUMMY_ENTITY_ID, DUMMY_ENTITY_VAL, FeatureView
from feast.infra.offline_stores import offline_utils
from feast.infra.offline_stores.contrib.postgres_offline_store.postgres_source import SavedDatasetPostgreSQLStorage
from feast.infra.offline_stores.offline_store import OfflineStore, RetrievalJob, RetrievalMetadata
from feast.infra.registry.registry import Registry
from feast.infra.utils.postgres.connection_utils import _get_conn, df_to_postgres_table, get_query_schema
from feast.infra.utils.postgres.postgres_config import PostgreSQLConfig
from feast.on_demand_feature_view import OnDemandFeatureView
from feast.repo_config import RepoConfig
from feast.saved_dataset import SavedDatasetStorage
from feast.type_map import pg_type_code_to_arrow
from feast.usage import log_exceptions_and_usage
from .postgres_source import PostgreSQLSource


def _get_entity_df_event_timestamp_range(entity_df: Union[(pd.DataFrame, str)], entity_df_event_timestamp_col: str, config: RepoConfig) -> Tuple[(datetime, datetime)]:
    if isinstance(entity_df, pd.DataFrame):
        entity_df_event_timestamp = entity_df.loc[:, entity_df_event_timestamp_col].infer_objects()
        if pd.api.types.is_string_dtype(entity_df_event_timestamp):
            entity_df_event_timestamp = pd.to_datetime(entity_df_event_timestamp, utc=True)
        entity_df_event_timestamp_range = (entity_df_event_timestamp.min().to_pydatetime(), entity_df_event_timestamp.max().to_pydatetime())
    elif isinstance(entity_df, str):
        with _get_conn(config.offline_store) as conn, conn.cursor() as cur:
            (cur.execute(f'SELECT MIN({entity_df_event_timestamp_col}) AS min, MAX({entity_df_event_timestamp_col}) AS max FROM ({entity_df}) as tmp_alias'),)
            res = cur.fetchone()
        entity_df_event_timestamp_range = (res[0], res[1])
    else:
        raise InvalidEntityType(type(entity_df))
    return entity_df_event_timestamp_range
