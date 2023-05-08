from typing import List, Tuple
import pandas as pd
import numpy as np


def parse_time(xtime: pd.Series) -> pd.DataFrame:
    '\n    Create time-based features\n    :param xtime: UNIX time\n    :return: Dataframe of time-based features\n    '
    result = pd.DataFrame()
    dtcol = pd.to_datetime(xtime, unit='s')
    result[f'{xtime.name}_year'] = dtcol.dt.year
    result[f'{xtime.name}_month'] = dtcol.dt.month
    result[f'{xtime.name}_dayofyear'] = dtcol.dt.dayofyear
    result[f'{xtime.name}_weekday'] = dtcol.dt.weekday
    result[f'{xtime.name}_hour'] = dtcol.dt.hour
    try:
        result[f'{xtime.name}_year'] = result[f'{xtime.name}_year'].astype('int16')
        result[f'{xtime.name}_month'] = result[f'{xtime.name}_month'].astype('int8')
        result[f'{xtime.name}_dayofyear'] = result[f'{xtime.name}_dayofyear'].astype('int16')
        result[f'{xtime.name}_weekday'] = result[f'{xtime.name}_weekday'].astype('int8')
        result[f'{xtime.name}_hour'] = result[f'{xtime.name}_hour'].astype('int8')
    except:
        pass
    return result
