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


def _upload_entity_df(spark_session: SparkSession, table_name: str, entity_df: Union[(pandas.DataFrame, str)], event_timestamp_col: str) -> None:
    if isinstance(entity_df, pd.DataFrame):
        entity_df[event_timestamp_col] = pd.to_datetime(entity_df[event_timestamp_col], utc=True)
        spark_session.createDataFrame(entity_df).createOrReplaceTempView(table_name)
        return
    elif isinstance(entity_df, str):
        spark_session.sql(entity_df).createOrReplaceTempView(table_name)
        return
    else:
        raise InvalidEntityType(type(entity_df))
