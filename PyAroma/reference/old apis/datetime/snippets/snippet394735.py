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
def pull_latest_from_table_or_query(config: RepoConfig, data_source: DataSource, join_key_columns: List[str], feature_name_columns: List[str], timestamp_field: str, created_timestamp_column: Optional[str], start_date: datetime, end_date: datetime, user: Optional[str]=None, auth: Optional[Authentication]=None, http_scheme: Optional[str]=None) -> TrinoRetrievalJob:
    assert isinstance(config.offline_store, TrinoOfflineStoreConfig)
    assert isinstance(data_source, TrinoSource)
    from_expression = data_source.get_table_query_string()
    partition_by_join_key_string = ', '.join(join_key_columns)
    if (partition_by_join_key_string != ''):
        partition_by_join_key_string = ('PARTITION BY ' + partition_by_join_key_string)
    timestamps = [timestamp_field]
    if created_timestamp_column:
        timestamps.append(created_timestamp_column)
    timestamp_desc_string = (' DESC, '.join(timestamps) + ' DESC')
    field_string = ', '.join(((join_key_columns + feature_name_columns) + timestamps))
    client = _get_trino_client(config=config, user=user, auth=auth, http_scheme=http_scheme)
    query = f'''
            SELECT
                {field_string}
                {(f', {repr(DUMMY_ENTITY_VAL)} AS {DUMMY_ENTITY_ID}' if (not join_key_columns) else '')}
            FROM (
                SELECT {field_string},
                ROW_NUMBER() OVER({partition_by_join_key_string} ORDER BY {timestamp_desc_string}) AS _feast_row
                FROM {from_expression}
                WHERE {timestamp_field} BETWEEN TIMESTAMP '{start_date}' AND TIMESTAMP '{end_date}'
            )
            WHERE _feast_row = 1
            '''
    return TrinoRetrievalJob(query=query, client=client, config=config, full_feature_names=False)
