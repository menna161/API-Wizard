import numpy as np
import pandas as pd
import CONSTANT
from sklearn.metrics import mean_squared_error
import math


def parse_time(xtime: pd.Series):
    result = pd.DataFrame()
    dtcol = pd.to_datetime(xtime, unit='s')
    result['year'] = dtcol.dt.year
    result['month'] = dtcol.dt.month
    result['day'] = dtcol.dt.day
    result['weekday'] = dtcol.dt.weekday
    result['hour'] = dtcol.dt.hour
    return result
