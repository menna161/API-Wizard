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


def assert_expected_arrow_types(provider: str, feature_dtype: str, feature_is_list: bool, historical_features: RetrievalJob):
    print('Asserting historical feature arrow types')
    historical_features_arrow = historical_features.to_arrow()
    print(historical_features_arrow)
    feature_list_dtype_to_expected_historical_feature_arrow_type = {'int32': pa.types.is_signed_integer, 'int64': pa.types.is_signed_integer, 'float': pa.types.is_float64, 'string': pa.types.is_string, 'bool': pa.types.is_boolean, 'date': pa.types.is_date, 'datetime': pa.types.is_timestamp}
    arrow_type_checker = feature_list_dtype_to_expected_historical_feature_arrow_type[feature_dtype]
    pa_type = historical_features_arrow.schema.field('value').type
    if feature_is_list:
        assert pa.types.is_list(pa_type)
        assert arrow_type_checker(pa_type.value_type)
    else:
        assert arrow_type_checker(pa_type)
