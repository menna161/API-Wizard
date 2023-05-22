import pandas as pd
import numpy as np


def parse_time(xtime: pd.Series):
    result = pd.DataFrame()
    dtcol = pd.to_datetime(xtime, unit='s')
    result[f'{xtime.name}'] = (dtcol.astype('int64') // (10 ** 9))
    result[f'{xtime.name}_year'] = dtcol.dt.year
    result[f'{xtime.name}_month'] = dtcol.dt.month
    result[f'{xtime.name}_day'] = dtcol.dt.day
    result[f'{xtime.name}_weekday'] = dtcol.dt.weekday
    result[f'{xtime.name}_hour'] = dtcol.dt.hour
    return result
