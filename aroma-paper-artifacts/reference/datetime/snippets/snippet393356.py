import itertools
from enum import Enum
import numpy as np
import pandas as pd
from pytz import FixedOffset, timezone, utc
from feast.infra.offline_stores.offline_utils import DEFAULT_ENTITY_DF_EVENT_TIMESTAMP_COL


def create_field_mapping_df(start_date, end_date) -> pd.DataFrame:
    '\n    Example df generated by this function:\n    | event_timestamp  | column_name | created          |\n    |------------------+-------------+------------------|\n    | 2021-03-17 19:00 | 99          | 2021-03-24 19:38 |\n    | 2021-03-17 19:00 | 22          | 2021-03-24 19:38 |\n    | 2021-03-17 19:00 | 7           | 2021-03-24 19:38 |\n    | 2021-03-17 19:00 | 45          | 2021-03-24 19:38 |\n    '
    size = 10
    df = pd.DataFrame()
    df['column_name'] = np.random.randint(1, 100, size=size).astype(np.int32)
    df[DEFAULT_ENTITY_DF_EVENT_TIMESTAMP_COL] = [_convert_event_timestamp(pd.Timestamp(dt, unit='ms', tz='UTC').round('ms'), EventTimestampType((idx % 4))) for (idx, dt) in enumerate(pd.date_range(start=start_date, end=end_date, periods=size))]
    df['created'] = pd.to_datetime(pd.Timestamp.now(tz=None).round('ms'))
    return df
