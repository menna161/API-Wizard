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


def assert_expected_historical_feature_types(feature_dtype: str, historical_features_df: pd.DataFrame):
    print('Asserting historical feature types')
    feature_dtype_to_expected_historical_feature_dtype = {'int32': (pd.api.types.is_integer_dtype,), 'int64': (pd.api.types.is_integer_dtype,), 'float': (pd.api.types.is_float_dtype,), 'string': (pd.api.types.is_string_dtype,), 'bool': (pd.api.types.is_bool_dtype, pd.api.types.is_object_dtype), 'datetime': (pd.api.types.is_datetime64_any_dtype,)}
    dtype_checkers = feature_dtype_to_expected_historical_feature_dtype[feature_dtype]
    assert any((check(historical_features_df.dtypes['value']) for check in dtype_checkers)), f"Failed to match feature type {historical_features_df.dtypes['value']} with checkers {dtype_checkers}"
