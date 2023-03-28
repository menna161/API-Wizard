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


@pytest.mark.integration
@pytest.mark.universal_online_stores(only=['sqlite'])
def test_feature_get_online_features_types_match(online_types_test_fixtures, environment):
    (config, data_source, fv) = online_types_test_fixtures
    entity = driver()
    fv = driver_feature_view(data_source=data_source, name='get_online_features_types_match', dtype=_get_feast_type(config.feature_dtype, config.feature_is_list))
    fs = environment.feature_store
    features = [(fv.name + ':value')]
    fs.apply([fv, entity])
    fs.materialize(environment.start_date, (environment.end_date - timedelta(hours=1)))
    online_features = fs.get_online_features(features=features, entity_rows=[{'driver_id': 1}]).to_dict()
    feature_list_dtype_to_expected_online_response_value_type = {'int32': int, 'int64': int, 'float': float, 'string': str, 'bool': bool, 'datetime': datetime}
    expected_dtype = feature_list_dtype_to_expected_online_response_value_type[config.feature_dtype]
    assert (len(online_features['value']) == 1)
    if config.feature_is_list:
        for feature in online_features['value']:
            assert isinstance(feature, list), 'Feature value should be a list'
            assert (config.has_empty_list or (len(feature) > 0)), 'List of values should not be empty'
            for element in feature:
                assert isinstance(element, expected_dtype)
    else:
        for feature in online_features['value']:
            assert isinstance(feature, expected_dtype)
