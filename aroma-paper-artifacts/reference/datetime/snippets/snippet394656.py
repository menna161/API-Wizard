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
@pytest.mark.universal_offline_stores
def test_feature_get_historical_features_types_match(offline_types_test_fixtures, environment):
    '\n    Note: to make sure this test works, we need to ensure that get_historical_features\n    returns at least one non-null row to make sure type inferral works. This can only\n    be achieved by carefully matching entity_df to the data fixtures.\n    '
    (config, data_source, fv) = offline_types_test_fixtures
    fs = environment.feature_store
    entity = driver()
    fv = driver_feature_view(data_source=data_source, name='get_historical_features_types_match', dtype=_get_feast_type(config.feature_dtype, config.feature_is_list))
    fs.apply([fv, entity])
    entity_df = pd.DataFrame()
    entity_df['driver_id'] = [1, 3]
    ts = pd.Timestamp(datetime.utcnow()).round('ms')
    entity_df['ts'] = [(ts - timedelta(hours=4)), (ts - timedelta(hours=2))]
    features = [f'{fv.name}:value']
    historical_features = fs.get_historical_features(entity_df=entity_df, features=features)
    historical_features_df = historical_features.to_df()
    print(historical_features_df)
    if config.feature_is_list:
        assert_feature_list_types(environment.test_repo_config.provider, config.feature_dtype, historical_features_df)
    else:
        assert_expected_historical_feature_types(config.feature_dtype, historical_features_df)
    assert_expected_arrow_types(environment.test_repo_config.provider, config.feature_dtype, config.feature_is_list, historical_features)
