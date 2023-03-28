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
def pull_all_from_table_or_query(config: RepoConfig, data_source: DataSource, join_key_columns: List[str], feature_name_columns: List[str], timestamp_field: str, start_date: datetime, end_date: datetime) -> RetrievalJob:
    '\n        Note that join_key_columns, feature_name_columns, timestamp_field, and\n        created_timestamp_column have all already been mapped to column names of the\n        source table and those column names are the values passed into this function.\n        '
    assert isinstance(config.offline_store, SparkOfflineStoreConfig)
    assert isinstance(data_source, SparkSource)
    warnings.warn('The spark offline store is an experimental feature in alpha development. This API is unstable and it could and most probably will be changed in the future.', RuntimeWarning)
    spark_session = get_spark_session_or_start_new_with_repoconfig(store_config=config.offline_store)
    fields = ', '.join(((join_key_columns + feature_name_columns) + [timestamp_field]))
    from_expression = data_source.get_table_query_string()
    start_date = start_date.astimezone(tz=utc)
    end_date = end_date.astimezone(tz=utc)
    query = f'''
            SELECT {fields}
            FROM {from_expression}
            WHERE {timestamp_field} BETWEEN TIMESTAMP '{start_date}' AND TIMESTAMP '{end_date}'
        '''
    return SparkRetrievalJob(spark_session=spark_session, query=query, full_feature_names=False, config=config)
