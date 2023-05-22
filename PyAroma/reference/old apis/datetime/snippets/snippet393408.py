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


def find_latest_record(records: List[Dict[(str, Any)]], ts_key: str, ts_start: datetime, ts_end: datetime, filter_keys: Optional[List[str]]=None, filter_values: Optional[List[Any]]=None) -> Dict[(str, Any)]:
    filter_keys = (filter_keys or [])
    filter_values = (filter_values or [])
    assert (len(filter_keys) == len(filter_values))
    found_record: Dict[(str, Any)] = {}
    for record in records:
        if (all([(record[filter_key] == filter_value) for (filter_key, filter_value) in zip(filter_keys, filter_values)]) and (ts_start <= record[ts_key] <= ts_end)):
            if ((not found_record) or (found_record[ts_key] < record[ts_key])):
                found_record = record
    return found_record
