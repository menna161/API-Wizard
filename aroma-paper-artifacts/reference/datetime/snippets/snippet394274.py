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


def _format_datetime(t: datetime) -> str:
    if t.tzinfo:
        t = t.astimezone(tz=utc)
    dt = t.strftime('%Y-%m-%d %H:%M:%S.%f')
    return dt
