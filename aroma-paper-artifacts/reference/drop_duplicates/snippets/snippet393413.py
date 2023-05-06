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


def validate_dataframes(expected_df: pd.DataFrame, actual_df: pd.DataFrame, sort_by: List[str], event_timestamp_column: Optional[str]=None, timestamp_precision: timedelta=timedelta(seconds=0)):
    expected_df = expected_df.sort_values(by=sort_by).drop_duplicates().reset_index(drop=True)
    actual_df = actual_df[expected_df.columns].sort_values(by=sort_by).drop_duplicates().reset_index(drop=True)
    if event_timestamp_column:
        expected_timestamp_col = expected_df[event_timestamp_column].to_frame()
        actual_timestamp_col = expected_df[event_timestamp_column].to_frame()
        expected_df = expected_df.drop(event_timestamp_column, axis=1)
        actual_df = actual_df.drop(event_timestamp_column, axis=1)
        if (event_timestamp_column in sort_by):
            sort_by.remove(event_timestamp_column)
        diffs = (expected_timestamp_col.to_numpy() - actual_timestamp_col.to_numpy())
        for diff in diffs:
            if isinstance(diff, np.ndarray):
                diff = diff[0]
            if isinstance(diff, np.timedelta64):
                assert (abs(diff) <= timestamp_precision.seconds)
            else:
                assert (abs(diff) <= timestamp_precision)
    pd_assert_frame_equal(expected_df, actual_df, check_dtype=False)
