import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import pandas as pd
import pyarrow as pa
import pytest
from feast.infra.offline_stores.offline_store import RetrievalJob
from feast.types import Array, Bool, FeastType, Float32, Float64, Int32, Int64, String, UnixTimestamp
from tests.data.data_creator import create_basic_driver_dataset
from tests.integration.feature_repos.universal.entities import driver
from tests.integration.feature_repos.universal.feature_views import driver_feature_view


def _get_feast_type(feature_dtype: str, feature_is_list: bool) -> FeastType:
    dtype: Optional[FeastType] = None
    if (feature_is_list is True):
        if (feature_dtype == 'int32'):
            dtype = Array(Int32)
        elif (feature_dtype == 'int64'):
            dtype = Array(Int64)
        elif (feature_dtype == 'float'):
            dtype = Array(Float32)
        elif (feature_dtype == 'bool'):
            dtype = Array(Bool)
        elif (feature_dtype == 'datetime'):
            dtype = Array(UnixTimestamp)
    elif (feature_dtype == 'int32'):
        dtype = Int32
    elif (feature_dtype == 'int64'):
        dtype = Int64
    elif (feature_dtype == 'float'):
        dtype = Float32
    elif (feature_dtype == 'bool'):
        dtype = Bool
    elif (feature_dtype == 'datetime'):
        dtype = UnixTimestamp
    assert dtype
    return dtype
