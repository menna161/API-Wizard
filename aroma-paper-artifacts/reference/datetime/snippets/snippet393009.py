import contextlib
import uuid
from datetime import datetime
from pathlib import Path
from typing import Callable, ContextManager, Dict, Iterator, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
import pyarrow
import pyarrow as pa
from pydantic import StrictStr
from pydantic.typing import Literal
from pytz import utc
from feast import OnDemandFeatureView
from feast.data_source import DataSource
from feast.errors import InvalidEntityType
from feast.feature_logging import LoggingConfig, LoggingSource
from feast.feature_view import DUMMY_ENTITY_ID, DUMMY_ENTITY_VAL, FeatureView
from feast.infra.offline_stores import offline_utils
from feast.infra.offline_stores.contrib.athena_offline_store.athena_source import AthenaLoggingDestination, AthenaSource, SavedDatasetAthenaStorage
from feast.infra.offline_stores.offline_store import OfflineStore, RetrievalJob, RetrievalMetadata
from feast.infra.registry.base_registry import BaseRegistry
from feast.infra.registry.registry import Registry
from feast.infra.utils import aws_utils
from feast.repo_config import FeastConfigBaseModel, RepoConfig
from feast.saved_dataset import SavedDatasetStorage
from feast.usage import log_exceptions_and_usage


def _get_entity_df_event_timestamp_range(entity_df: Union[(pd.DataFrame, str)], entity_df_event_timestamp_col: str, athena_client, config: RepoConfig) -> Tuple[(datetime, datetime)]:
    if isinstance(entity_df, pd.DataFrame):
        entity_df_event_timestamp = entity_df.loc[:, entity_df_event_timestamp_col].infer_objects()
        if pd.api.types.is_string_dtype(entity_df_event_timestamp):
            entity_df_event_timestamp = pd.to_datetime(entity_df_event_timestamp, utc=True)
        entity_df_event_timestamp_range = (entity_df_event_timestamp.min().to_pydatetime(), entity_df_event_timestamp.max().to_pydatetime())
    elif isinstance(entity_df, str):
        statement_id = aws_utils.execute_athena_query(athena_client, config.offline_store.data_source, config.offline_store.database, config.offline_store.workgroup, f'SELECT MIN({entity_df_event_timestamp_col}) AS min, MAX({entity_df_event_timestamp_col}) AS max FROM ({entity_df})')
        res = aws_utils.get_athena_query_result(athena_client, statement_id)
        entity_df_event_timestamp_range = (datetime.strptime(res['Rows'][1]['Data'][0]['VarCharValue'], '%Y-%m-%d %H:%M:%S.%f'), datetime.strptime(res['Rows'][1]['Data'][1]['VarCharValue'], '%Y-%m-%d %H:%M:%S.%f'))
    else:
        raise InvalidEntityType(type(entity_df))
    return entity_df_event_timestamp_range
