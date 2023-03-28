import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pytz import FixedOffset, timezone, utc
from random import randint
from enum import Enum
from sqlalchemy import create_engine, DateTime
from datetime import datetime


def create_driver_hourly_stats_df(drivers, start_date, end_date) -> pd.DataFrame:
    '\n    Example df generated by this function:\n    | datetime         | driver_id | conv_rate | acc_rate | avg_daily_trips | created          |\n    |------------------+-----------+-----------+----------+-----------------+------------------|\n    | 2021-03-17 19:31 |     5010  | 0.229297  | 0.685843 | 861             | 2021-03-24 19:34 |\n    | 2021-03-17 20:31 |     5010  | 0.781655  | 0.861280 | 769             | 2021-03-24 19:34 |\n    | 2021-03-17 21:31 |     5010  | 0.150333  | 0.525581 | 778             | 2021-03-24 19:34 |\n    | 2021-03-17 22:31 |     5010  | 0.951701  | 0.228883 | 570             | 2021-03-24 19:34 |\n    | 2021-03-17 23:31 |     5010  | 0.819598  | 0.262503 | 473             | 2021-03-24 19:34 |\n    |                  |      ...  |      ...  |      ... | ...             |                  |\n    | 2021-03-24 16:31 |     5001  | 0.061585  | 0.658140 | 477             | 2021-03-24 19:34 |\n    | 2021-03-24 17:31 |     5001  | 0.088949  | 0.303897 | 618             | 2021-03-24 19:34 |\n    | 2021-03-24 18:31 |     5001  | 0.096652  | 0.747421 | 480             | 2021-03-24 19:34 |\n    | 2021-03-17 19:31 |     5005  | 0.142936  | 0.707596 | 466             | 2021-03-24 19:34 |\n    | 2021-03-17 19:31 |     5005  | 0.142936  | 0.707596 | 466             | 2021-03-24 19:34 |\n    '
    df_hourly = pd.DataFrame({'datetime': [pd.Timestamp(dt, unit='ms', tz='UTC').round('ms') for dt in pd.date_range(start=start_date, end=end_date, freq='1H', closed='left')]})
    df_all_drivers = pd.DataFrame()
    dates = df_hourly['datetime'].map(pd.Timestamp.date).unique()
    for driver in drivers:
        df_hourly_copy = df_hourly.copy()
        df_hourly_copy['driver_id'] = driver
        for date in dates:
            df_hourly_copy.loc[((df_hourly_copy['datetime'].map(pd.Timestamp.date) == date), 'avg_daily_trips')] = randint(10, 30)
        df_all_drivers = pd.concat([df_hourly_copy, df_all_drivers])
    df_all_drivers.reset_index(drop=True, inplace=True)
    rows = df_all_drivers['datetime'].count()
    df_all_drivers['conv_rate'] = np.random.random(size=rows).astype(np.float32)
    df_all_drivers['acc_rate'] = np.random.random(size=rows).astype(np.float32)
    df_all_drivers['created'] = pd.to_datetime(pd.Timestamp.now(tz=None).round('ms'))
    late_row = df_all_drivers.iloc[int((rows / 2))]
    df_all_drivers = df_all_drivers.append(late_row).append(late_row)
    return df_all_drivers
