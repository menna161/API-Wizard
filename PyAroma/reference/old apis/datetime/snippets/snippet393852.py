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
def pull_all_from_table_or_query(config: RepoConfig, data_source: DataSource, join_key_columns: List[str], feature_name_columns: List[str], timestamp_field: str, start_date: datetime, end_date: datetime) -> RetrievalJob:
    assert isinstance(config.offline_store, PostgreSQLOfflineStoreConfig)
    assert isinstance(data_source, PostgreSQLSource)
    from_expression = data_source.get_table_query_string()
    field_string = ', '.join(((join_key_columns + feature_name_columns) + [timestamp_field]))
    start_date = start_date.astimezone(tz=utc)
    end_date = end_date.astimezone(tz=utc)
    query = f'''
            SELECT {field_string}
            FROM {from_expression} AS paftoq_alias
            WHERE "{timestamp_field}" BETWEEN '{start_date}'::timestamptz AND '{end_date}'::timestamptz
        '''
    return PostgreSQLRetrievalJob(query=query, config=config, full_feature_names=False, on_demand_feature_views=None)
