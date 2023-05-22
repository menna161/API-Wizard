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


def assert_feature_service_entity_mapping_correctness(store, feature_service, full_feature_names, entity_df, expected_df, event_timestamp):
    if full_feature_names:
        job_from_df = store.get_historical_features(entity_df=entity_df, features=feature_service, full_feature_names=full_feature_names)
        actual_df_from_df_entities = job_from_df.to_df()
        expected_df: pd.DataFrame = expected_df.sort_values(by=[event_timestamp, 'order_id', 'driver_id', 'customer_id', 'origin_id', 'destination_id']).drop_duplicates().reset_index(drop=True)
        expected_df = expected_df[[event_timestamp, 'order_id', 'driver_id', 'customer_id', 'origin_id', 'destination_id', 'origin__temperature', 'destination__temperature']]
        validate_dataframes(expected_df, actual_df_from_df_entities, sort_by=[event_timestamp, 'order_id', 'driver_id', 'customer_id', 'origin_id', 'destination_id'], event_timestamp_column=event_timestamp, timestamp_precision=timedelta(milliseconds=1))
    else:
        with pytest.raises(FeatureNameCollisionError):
            job_from_df = store.get_historical_features(entity_df=entity_df, features=feature_service, full_feature_names=full_feature_names)
