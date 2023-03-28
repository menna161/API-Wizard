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
def get_historical_features(config: RepoConfig, feature_views: List[FeatureView], feature_refs: List[str], entity_df: Union[(pandas.DataFrame, str)], registry: BaseRegistry, project: str, full_feature_names: bool=False) -> RetrievalJob:
    warnings.warn('The Azure Synapse + Azure SQL offline store is an experimental feature in alpha development. Some functionality may still be unstable so functionality can change in the future.', RuntimeWarning)
    expected_join_keys = _get_join_keys(project, feature_views, registry)
    assert isinstance(config.offline_store, MsSqlServerOfflineStoreConfig)
    engine = make_engine(config.offline_store)
    if isinstance(entity_df, pandas.DataFrame):
        entity_df_event_timestamp_col = offline_utils.infer_event_timestamp_from_entity_df(dict(zip(list(entity_df.columns), list(entity_df.dtypes))))
        entity_df[entity_df_event_timestamp_col] = pandas.to_datetime(entity_df[entity_df_event_timestamp_col], utc=True).fillna(pandas.Timestamp.now())
    elif isinstance(entity_df, str):
        raise ValueError('string entities are currently not supported in the MsSQL offline store.')
    (table_schema, table_name) = _upload_entity_df_into_sqlserver_and_get_entity_schema(engine, config, entity_df, full_feature_names=full_feature_names)
    _assert_expected_columns_in_sqlserver(expected_join_keys, entity_df_event_timestamp_col, table_schema)
    entity_df_event_timestamp_range = _get_entity_df_event_timestamp_range(entity_df, entity_df_event_timestamp_col, engine)
    query_context = get_feature_view_query_context(feature_refs, feature_views, registry, project, entity_df_timestamp_range=entity_df_event_timestamp_range)
    query = build_point_in_time_query(query_context, left_table_query_string=table_name, entity_df_event_timestamp_col=entity_df_event_timestamp_col, entity_df_columns=table_schema.keys(), full_feature_names=full_feature_names, query_template=MULTIPLE_FEATURE_VIEW_POINT_IN_TIME_JOIN)
    query = query.replace('`', '')
    job = MsSqlServerRetrievalJob(query=query, engine=engine, config=config.offline_store, full_feature_names=full_feature_names, on_demand_feature_views=registry.list_on_demand_feature_views(project))
    return job
