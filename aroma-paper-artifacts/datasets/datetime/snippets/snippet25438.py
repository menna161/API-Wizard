import os
import re
import zipfile
import pysftp
from pathlib import Path
from time import time
import pandas as pd
import numpy as np
import quandl
from scipy.io import loadmat
from pyfolio.timeseries import cum_returns
from urllib.request import urlretrieve
import plistlib
import nest_asyncio
from datetime import datetime
from option_utilities import USZeroYieldCurve, write_feather, read_feather, matlab2datetime, get_asset
from ib_insync import IB, util, Index
from twilio.rest import Client


def _rolled_future_return(self):
    'Returns arithmetic return from long position in vix future'
    expiry_dates = pd.to_datetime(self.raw_tsm_df['exp1'].astype(int), format='%Y%m%d')
    returns = self._expiry_returns
    days_2_exp = self._expiration_days_2_expiry
    if (self.expiry_type == 'eom'):
        eom_dates = returns.index[returns.reset_index().groupby(returns.index.to_period('M'))['index'].idxmax()]
        last_month_end = (eom_dates[(- 1)] + pd.offsets.MonthEnd(0))
        eom_dates = eom_dates[:(- 1)]
        eom_dates = eom_dates.insert((- 1), last_month_end)
        roll_dates = eom_dates.sort_values()
    else:
        expiry_dates_unique = pd.to_datetime(self.raw_tsm_df['exp1'].unique().astype(int), format='%Y%m%d')
        roll_dates = (expiry_dates_unique - pd.offsets.BDay(self.expiry_type))
    expiry_for_roll = []
    for dts in expiry_dates:
        idx = roll_dates.get_loc(dts, method='ffill')
        expiry_for_roll.append(roll_dates[idx])
    day_diff = (expiry_dates.index - pd.DatetimeIndex(expiry_for_roll))
    front_month_bool = (day_diff.days < 0)
    back_month_bool = (~ front_month_bool)
    rolled_return = pd.concat([returns['close2'][back_month_bool], returns['close1'][front_month_bool]], axis=0).sort_index()
    rolled_return[0] = np.nan
    rolled_expiries = pd.concat([self.raw_tsm_df['exp2'][back_month_bool], self.raw_tsm_df['exp1'][front_month_bool]], axis=0).sort_index()
    days_2_exp = pd.concat([days_2_exp['exp2'][back_month_bool], days_2_exp['exp1'][front_month_bool]], axis=0).sort_index()
    rolled_future = pd.concat([self.raw_tsm_df['close2'][back_month_bool], self.raw_tsm_df['close1'][front_month_bool]], axis=0).sort_index()
    return (rolled_return, rolled_expiries, days_2_exp, rolled_future)
