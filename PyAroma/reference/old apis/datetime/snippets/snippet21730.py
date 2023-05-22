import logging
from datetime import datetime
from typing import Dict, List
import pandas as pd
from django.conf import settings
from data.models import Events, SeenByDay, SeenByHour


def prepare_df_datetime_index(df: pd.DataFrame, time_column='time_seen') -> pd.DataFrame:
    '\n    Utility function which prepares an event dataframe to become time series data\n    '
    df.astype(str, inplace=True)
    df.rename(columns={time_column: 'time'}, inplace=True)
    df.index = df['time']
    del df['time']
    if (not df.index.empty):
        if (df.index.tzinfo is not None):
            df.index = df.index.tz_convert(settings.TIME_ZONE)
        else:
            df.index = df.index.tz_localize(settings.TIME_ZONE)
    for field_name in ('id', 'box_id', 'total_packets'):
        if (field_name in df.columns):
            df.drop(field_name, 1, inplace=True)
    return df
