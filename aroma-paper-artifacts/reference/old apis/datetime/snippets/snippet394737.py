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


@staticmethod
@log_exceptions_and_usage(offline_store='trino')
def pull_all_from_table_or_query(config: RepoConfig, data_source: DataSource, join_key_columns: List[str], feature_name_columns: List[str], timestamp_field: str, start_date: datetime, end_date: datetime, user: Optional[str]=None, auth: Optional[Authentication]=None, http_scheme: Optional[str]=None) -> RetrievalJob:
    assert isinstance(config.offline_store, TrinoOfflineStoreConfig)
    assert isinstance(data_source, TrinoSource)
    from_expression = data_source.get_table_query_string()
    client = _get_trino_client(config=config, user=user, auth=auth, http_scheme=http_scheme)
    field_string = ', '.join(((join_key_columns + feature_name_columns) + [timestamp_field]))
    query = f'''
            SELECT {field_string}
            FROM {from_expression}
            WHERE {timestamp_field} BETWEEN TIMESTAMP '{start_date}'  AND TIMESTAMP '{end_date}'
        '''
    return TrinoRetrievalJob(query=query, client=client, config=config, full_feature_names=False)
