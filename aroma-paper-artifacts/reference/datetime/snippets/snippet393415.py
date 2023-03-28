from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal as pd_assert_frame_equal
from pytz import utc
from feast import FeatureService, FeatureStore, utils
from feast.errors import FeatureNameCollisionError
from feast.feature_view import FeatureView


def validate_online_features(store: FeatureStore, driver_df: pd.DataFrame, max_date: datetime):
    'Assert that features in online store are up to date with `max_date` date.'
    response = store.get_online_features(features=['driver_hourly_stats:conv_rate', 'driver_hourly_stats:avg_daily_trips', 'global_daily_stats:num_rides', 'global_daily_stats:avg_ride_length'], entity_rows=[{'driver_id': 1001}], full_feature_names=True)
    assert (response.proto.results[list(response.proto.metadata.feature_names.val).index('driver_hourly_stats__conv_rate')].values[0].float_val > 0), response.to_dict()
    result = response.to_dict()
    assert (len(result) == 5)
    assert ('driver_hourly_stats__avg_daily_trips' in result)
    assert ('driver_hourly_stats__conv_rate' in result)
    assert (abs((result['driver_hourly_stats__conv_rate'][0] - get_last_feature_row(driver_df, 1001, max_date)['conv_rate'])) < 0.01)
    assert ('global_daily_stats__num_rides' in result)
    assert ('global_daily_stats__avg_ride_length' in result)
    odfvs = store.list_on_demand_feature_views()
    if (odfvs and (odfvs[0].name == 'conv_rate_plus_100')):
        response = store.get_online_features(features=['conv_rate_plus_100:conv_rate_plus_100', 'conv_rate_plus_100:conv_rate_plus_val_to_add'], entity_rows=[{'driver_id': 1001, 'val_to_add': 100}], full_feature_names=True)
        assert (response.proto.results[list(response.proto.metadata.feature_names.val).index('conv_rate_plus_100__conv_rate_plus_100')].values[0].double_val > 0)
        result = response.to_dict()
        assert (len(result) == 3)
        assert ('conv_rate_plus_100__conv_rate_plus_100' in result)
        assert ('conv_rate_plus_100__conv_rate_plus_val_to_add' in result)
        assert (abs((result['conv_rate_plus_100__conv_rate_plus_100'][0] - (get_last_feature_row(driver_df, 1001, max_date)['conv_rate'] + 100))) < 0.01)
        assert (abs((result['conv_rate_plus_100__conv_rate_plus_val_to_add'][0] - (get_last_feature_row(driver_df, 1001, max_date)['conv_rate'] + 100))) < 0.01)
