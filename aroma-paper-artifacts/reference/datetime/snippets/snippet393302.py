from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
from pytz import timezone, utc
from feast.types import FeastType, Float32, Int32, Int64, String


def create_basic_driver_dataset(entity_type: FeastType=Int32, feature_dtype: str=None, feature_is_list: bool=False, list_has_empty_list: bool=False) -> pd.DataFrame:
    now = datetime.utcnow().replace(microsecond=0, second=0, minute=0)
    ts = pd.Timestamp(now).round('ms')
    data = {'driver_id': get_entities_for_feast_type(entity_type), 'value': get_feature_values_for_dtype(feature_dtype, feature_is_list, list_has_empty_list), 'ts_1': [(ts - timedelta(hours=4)), ts, (ts - timedelta(hours=3)), (ts - timedelta(hours=4)).replace(tzinfo=utc).astimezone(tz=timezone('Europe/Berlin')), (ts - timedelta(hours=1)).replace(tzinfo=utc).astimezone(tz=timezone('US/Pacific'))], 'created_ts': [ts, ts, ts, ts, ts]}
    return pd.DataFrame.from_dict(data)
