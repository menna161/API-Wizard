import uuid
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
import pyarrow
from pydantic import StrictStr
from trino.auth import Authentication
from feast.data_source import DataSource
from feast.errors import InvalidEntityType
from feast.feature_view import DUMMY_ENTITY_ID, DUMMY_ENTITY_VAL, FeatureView
from feast.infra.offline_stores import offline_utils
from feast.infra.offline_stores.contrib.trino_offline_store.connectors.upload import upload_pandas_dataframe_to_trino
from feast.infra.offline_stores.contrib.trino_offline_store.trino_queries import Trino
from feast.infra.offline_stores.contrib.trino_offline_store.trino_source import SavedDatasetTrinoStorage, TrinoSource
from feast.infra.offline_stores.offline_store import OfflineStore, RetrievalJob, RetrievalMetadata
from feast.infra.registry.registry import Registry
from feast.on_demand_feature_view import OnDemandFeatureView
from feast.repo_config import FeastConfigBaseModel, RepoConfig
from feast.saved_dataset import SavedDatasetStorage
from feast.usage import log_exceptions_and_usage


def _get_entity_df_event_timestamp_range(entity_df: Union[(pd.DataFrame, str)], entity_df_event_timestamp_col: str, client: Trino) -> Tuple[(datetime, datetime)]:
    if (type(entity_df) is str):
        results = client.execute_query(f'SELECT MIN({entity_df_event_timestamp_col}) AS min, MAX({entity_df_event_timestamp_col}) AS max FROM ({entity_df})')
        entity_df_event_timestamp_range = (pd.to_datetime(results.data[0][0]).to_pydatetime(), pd.to_datetime(results.data[0][1]).to_pydatetime())
    elif isinstance(entity_df, pd.DataFrame):
        entity_df_event_timestamp = entity_df.loc[:, entity_df_event_timestamp_col].infer_objects()
        if pd.api.types.is_string_dtype(entity_df_event_timestamp):
            entity_df_event_timestamp = pd.to_datetime(entity_df_event_timestamp, utc=True)
        entity_df_event_timestamp_range = (entity_df_event_timestamp.min().to_pydatetime(), entity_df_event_timestamp.max().to_pydatetime())
    else:
        raise InvalidEntityType(type(entity_df))
    return entity_df_event_timestamp_range
