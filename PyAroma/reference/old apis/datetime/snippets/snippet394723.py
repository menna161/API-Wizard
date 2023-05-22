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


def _upload_entity_df_and_get_entity_schema(client: Trino, table_name: str, entity_df: Union[(pd.DataFrame, str)], connector: Dict[(str, str)]) -> Dict[(str, np.dtype)]:
    'Uploads a Pandas entity dataframe into a Trino table and returns the resulting table'
    if (type(entity_df) is str):
        client.execute_query(f'CREATE TABLE {table_name} AS ({entity_df})')
        results = client.execute_query(f'SELECT * FROM {table_name} LIMIT 1')
        limited_entity_df = pd.DataFrame(data=results.data, columns=results.columns_names)
        for (col_name, col_type) in results.schema.items():
            if (col_type == 'timestamp'):
                limited_entity_df[col_name] = pd.to_datetime(limited_entity_df[col_name])
        entity_schema = dict(zip(limited_entity_df.columns, limited_entity_df.dtypes))
        return entity_schema
    elif isinstance(entity_df, pd.DataFrame):
        upload_pandas_dataframe_to_trino(client=client, df=entity_df, table=table_name, connector_args=connector)
        entity_schema = dict(zip(entity_df.columns, entity_df.dtypes))
        return entity_schema
    else:
        raise InvalidEntityType(type(entity_df))
