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


def _get_entity_df_event_timestamp_range(entity_df: Union[(pd.DataFrame, str)], entity_df_event_timestamp_col: str, spark_session: SparkSession) -> Tuple[(datetime, datetime)]:
    if isinstance(entity_df, pd.DataFrame):
        entity_df_event_timestamp = entity_df.loc[:, entity_df_event_timestamp_col].infer_objects()
        if pd.api.types.is_string_dtype(entity_df_event_timestamp):
            entity_df_event_timestamp = pd.to_datetime(entity_df_event_timestamp, utc=True)
        entity_df_event_timestamp_range = (entity_df_event_timestamp.min().to_pydatetime(), entity_df_event_timestamp.max().to_pydatetime())
    elif isinstance(entity_df, str):
        df = spark_session.sql(entity_df).select(entity_df_event_timestamp_col)
        if df.rdd.isEmpty():
            raise EntitySQLEmptyResults(entity_df)
        entity_df_event_timestamp_range = (df.agg({entity_df_event_timestamp_col: 'min'}).collect()[0][0], df.agg({entity_df_event_timestamp_col: 'max'}).collect()[0][0])
    else:
        raise InvalidEntityType(type(entity_df))
    return entity_df_event_timestamp_range