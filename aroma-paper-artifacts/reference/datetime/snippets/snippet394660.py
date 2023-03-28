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


def assert_feature_list_types(provider: str, feature_dtype: str, historical_features_df: pd.DataFrame):
    print('Asserting historical feature list types')
    feature_list_dtype_to_expected_historical_feature_list_dtype: Dict[(str, Union[(type, Tuple[(Union[(type, Tuple[(Any, ...)])], ...)])])] = {'int32': (int, np.int64), 'int64': (int, np.int64), 'float': float, 'string': str, 'bool': (bool, np.bool_), 'datetime': (np.datetime64, datetime)}
    expected_dtype = feature_list_dtype_to_expected_historical_feature_list_dtype[feature_dtype]
    assert pd.api.types.is_object_dtype(historical_features_df.dtypes['value'])
    for feature in historical_features_df.value:
        assert isinstance(feature, (np.ndarray, list))
        for element in feature:
            assert isinstance(element, expected_dtype)
