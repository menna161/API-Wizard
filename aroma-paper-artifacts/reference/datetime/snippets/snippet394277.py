import os
import tempfile
import uuid
import warnings
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas
import pandas as pd
import pyarrow
import pyarrow.parquet as pq
import pyspark
from pydantic import StrictStr
from pyspark import SparkConf
from pyspark.sql import SparkSession
from pytz import utc
from feast import FeatureView, OnDemandFeatureView
from feast.data_source import DataSource
from feast.errors import EntitySQLEmptyResults, InvalidEntityType
from feast.feature_view import DUMMY_ENTITY_ID, DUMMY_ENTITY_VAL
from feast.infra.offline_stores import offline_utils
from feast.infra.offline_stores.contrib.spark_offline_store.spark_source import SavedDatasetSparkStorage, SparkSource
from feast.infra.offline_stores.offline_store import OfflineStore, RetrievalJob, RetrievalMetadata
from feast.infra.registry.registry import Registry
from feast.infra.utils import aws_utils
from feast.repo_config import FeastConfigBaseModel, RepoConfig
from feast.saved_dataset import SavedDatasetStorage
from feast.type_map import spark_schema_to_np_dtypes
from feast.usage import log_exceptions_and_usage


@staticmethod
@log_exceptions_and_usage(offline_store='spark')
def pull_latest_from_table_or_query(config: RepoConfig, data_source: DataSource, join_key_columns: List[str], feature_name_columns: List[str], timestamp_field: str, created_timestamp_column: Optional[str], start_date: datetime, end_date: datetime) -> RetrievalJob:
    spark_session = get_spark_session_or_start_new_with_repoconfig(config.offline_store)
    assert isinstance(config.offline_store, SparkOfflineStoreConfig)
    assert isinstance(data_source, SparkSource)
    warnings.warn('The spark offline store is an experimental feature in alpha development. Some functionality may still be unstable so functionality can change in the future.', RuntimeWarning)
    print('Pulling latest features from spark offline store')
    from_expression = data_source.get_table_query_string()
    partition_by_join_key_string = ', '.join(join_key_columns)
    if (partition_by_join_key_string != ''):
        partition_by_join_key_string = ('PARTITION BY ' + partition_by_join_key_string)
    timestamps = [timestamp_field]
    if created_timestamp_column:
        timestamps.append(created_timestamp_column)
    timestamp_desc_string = (' DESC, '.join(timestamps) + ' DESC')
    field_string = ', '.join(((join_key_columns + feature_name_columns) + timestamps))
    start_date_str = _format_datetime(start_date)
    end_date_str = _format_datetime(end_date)
    query = f'''
                SELECT
                    {field_string}
                    {(f', {repr(DUMMY_ENTITY_VAL)} AS {DUMMY_ENTITY_ID}' if (not join_key_columns) else '')}
                FROM (
                    SELECT {field_string},
                    ROW_NUMBER() OVER({partition_by_join_key_string} ORDER BY {timestamp_desc_string}) AS feast_row_
                    FROM {from_expression} t1
                    WHERE {timestamp_field} BETWEEN TIMESTAMP('{start_date_str}') AND TIMESTAMP('{end_date_str}')
                ) t2
                WHERE feast_row_ = 1
                '''
    return SparkRetrievalJob(spark_session=spark_session, query=query, config=config, full_feature_names=False, on_demand_feature_views=None)
