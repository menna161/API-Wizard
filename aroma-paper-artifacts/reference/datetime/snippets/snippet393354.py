import itertools
from enum import Enum
import numpy as np
import pandas as pd
from pytz import FixedOffset, timezone, utc
from feast.infra.offline_stores.offline_utils import DEFAULT_ENTITY_DF_EVENT_TIMESTAMP_COL


def create_location_stats_df(locations, start_date, end_date) -> pd.DataFrame:
    '\n    Example df generated by this function:\n\n    | event_timestamp  | location_id | temperature | created          |\n    +------------------+-------------+-------------+------------------+\n    | 2021-03-17 19:31 |           1 |          74 | 2021-03-24 19:38 |\n    | 2021-03-17 20:31 |          24 |          63 | 2021-03-24 19:38 |\n    | 2021-03-17 21:31 |          19 |          65 | 2021-03-24 19:38 |\n    | 2021-03-17 22:31 |          35 |          86 | 2021-03-24 19:38 |\n    '
    df_hourly = pd.DataFrame({'event_timestamp': [pd.Timestamp(dt, unit='ms', tz='UTC').round('ms') for dt in pd.date_range(start=start_date, end=end_date, freq='1H', inclusive='left')]})
    df_all_locations = pd.DataFrame()
    for location in locations:
        df_hourly_copy = df_hourly.copy()
        df_hourly_copy['location_id'] = location
        df_all_locations = pd.concat([df_hourly_copy, df_all_locations])
    df_all_locations.reset_index(drop=True, inplace=True)
    rows = df_all_locations['event_timestamp'].count()
    df_all_locations['temperature'] = np.random.randint(50, 100, size=rows).astype(np.int32)
    df_all_locations['created'] = pd.to_datetime(pd.Timestamp.now(tz=None).round('ms'))
    return df_all_locations
