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


def get_last_feature_row(df: pd.DataFrame, driver_id, max_date: datetime):
    'Manually extract last feature value from a dataframe for a given driver_id with up to `max_date` date'
    filtered = df[((df['driver_id'] == driver_id) & (df['event_timestamp'] < max_date.replace(tzinfo=utc)))]
    max_ts = filtered.loc[filtered['event_timestamp'].idxmax()]['event_timestamp']
    filtered_by_ts = filtered[(filtered['event_timestamp'] == max_ts)]
    return filtered_by_ts.loc[filtered_by_ts['created'].idxmax()]
