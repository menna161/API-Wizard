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


@staticmethod
@log_exceptions_and_usage(offline_store='athena')
def pull_latest_from_table_or_query(config: RepoConfig, data_source: DataSource, join_key_columns: List[str], feature_name_columns: List[str], timestamp_field: str, created_timestamp_column: Optional[str], start_date: datetime, end_date: datetime) -> RetrievalJob:
    assert isinstance(config.offline_store, AthenaOfflineStoreConfig)
    assert isinstance(data_source, AthenaSource)
    from_expression = data_source.get_table_query_string(config)
    partition_by_join_key_string = ', '.join(join_key_columns)
    if (partition_by_join_key_string != ''):
        partition_by_join_key_string = ('PARTITION BY ' + partition_by_join_key_string)
    timestamp_columns = [timestamp_field]
    if created_timestamp_column:
        timestamp_columns.append(created_timestamp_column)
    timestamp_desc_string = (' DESC, '.join(timestamp_columns) + ' DESC')
    field_string = ', '.join(((join_key_columns + feature_name_columns) + timestamp_columns))
    date_partition_column = data_source.date_partition_column
    athena_client = aws_utils.get_athena_data_client(config.offline_store.region)
    s3_resource = aws_utils.get_s3_resource(config.offline_store.region)
    start_date = start_date.astimezone(tz=utc)
    end_date = end_date.astimezone(tz=utc)
    query = f'''
            SELECT
                {field_string}
                {(f', {repr(DUMMY_ENTITY_VAL)} AS {DUMMY_ENTITY_ID}' if (not join_key_columns) else '')}
            FROM (
                SELECT {field_string},
                ROW_NUMBER() OVER({partition_by_join_key_string} ORDER BY {timestamp_desc_string}) AS _feast_row
                FROM {from_expression}
                WHERE {timestamp_field} BETWEEN TIMESTAMP '{start_date.strftime('%Y-%m-%d %H:%M:%S')}' AND TIMESTAMP '{end_date.strftime('%Y-%m-%d %H:%M:%S')}'
                {((((((((('AND ' + date_partition_column) + " >= '") + start_date.strftime('%Y-%m-%d')) + "' AND ") + date_partition_column) + " <= '") + end_date.strftime('%Y-%m-%d')) + "' ") if ((date_partition_column != '') and (date_partition_column is not None)) else '')}
            )
            WHERE _feast_row = 1
            '''
    return AthenaRetrievalJob(query=query, athena_client=athena_client, s3_resource=s3_resource, config=config, full_feature_names=False)
