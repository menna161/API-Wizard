from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
from pytz import timezone, utc
from feast.types import FeastType, Float32, Int32, Int64, String


def get_feature_values_for_dtype(dtype: Optional[str], is_list: bool, has_empty_list: bool) -> List:
    if (dtype is None):
        return [0.1, None, 0.3, 4, 5]
    dtype_map: Dict[(str, List)] = {'int32': [1, 2, 3, 4, 5], 'int64': [1, 2, 3, 4, 5], 'float': [1.0, None, 3.0, 4.0, 5.0], 'string': ['1', None, '3', '4', '5'], 'bool': [True, None, False, True, False], 'datetime': [datetime(1980, 1, 1), None, datetime(1981, 1, 1), datetime(1982, 1, 1), datetime(1982, 1, 1)]}
    non_list_val = dtype_map[dtype]
    if is_list:
        if has_empty_list:
            return ([[] for n in non_list_val[:(- 1)]] + [non_list_val[(- 1):]])
        return [([n, n] if (n is not None) else None) for n in non_list_val]
    else:
        return non_list_val
