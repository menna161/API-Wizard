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


@staticmethod
@log_exceptions_and_usage(offline_store='postgres')
def pull_latest_from_table_or_query(config: RepoConfig, data_source: DataSource, join_key_columns: List[str], feature_name_columns: List[str], timestamp_field: str, created_timestamp_column: Optional[str], start_date: datetime, end_date: datetime) -> RetrievalJob:
    assert isinstance(config.offline_store, PostgreSQLOfflineStoreConfig)
    assert isinstance(data_source, PostgreSQLSource)
    from_expression = data_source.get_table_query_string()
    partition_by_join_key_string = ', '.join(_append_alias(join_key_columns, 'a'))
    if (partition_by_join_key_string != ''):
        partition_by_join_key_string = ('PARTITION BY ' + partition_by_join_key_string)
    timestamps = [timestamp_field]
    if created_timestamp_column:
        timestamps.append(created_timestamp_column)
    timestamp_desc_string = (' DESC, '.join(_append_alias(timestamps, 'a')) + ' DESC')
    a_field_string = ', '.join(_append_alias(((join_key_columns + feature_name_columns) + timestamps), 'a'))
    b_field_string = ', '.join(_append_alias(((join_key_columns + feature_name_columns) + timestamps), 'b'))
    query = f'''
            SELECT
                {b_field_string}
                {(f', {repr(DUMMY_ENTITY_VAL)} AS {DUMMY_ENTITY_ID}' if (not join_key_columns) else '')}
            FROM (
                SELECT {a_field_string},
                ROW_NUMBER() OVER({partition_by_join_key_string} ORDER BY {timestamp_desc_string}) AS _feast_row
                FROM ({from_expression}) a
                WHERE a."{timestamp_field}" BETWEEN '{start_date}'::timestamptz AND '{end_date}'::timestamptz
            ) b
            WHERE _feast_row = 1
            '''
    return PostgreSQLRetrievalJob(query=query, config=config, full_feature_names=False, on_demand_feature_views=None)
