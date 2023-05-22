import pyfolio as pf
import numpy as np
import pandas as pd
from statsmodels.tsa.arima_model import ARMA
import statsmodels.tsa.api as smt
import statsmodels.api as sm
import scipy.stats as scs
import matplotlib.gridspec as gridspec
from ib_insync import Future, util
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import re
import zipfile
from option_utilities import read_feather
from pyfolio.timeseries import cum_returns
from spx_data_update import UpdateSP500Data, ImpliedVolatilityHistory, SP500Index, IbWrapper, GetRawCBOEOptionData
from option_utilities import PlotConstants, chart_format


def rolled_future(self):
    'Returns continuous return, price index, expiries and days 2 expiry for vix future rolled according to\n        expiry type'
    expiry_dates = self.expirations['expiry1']
    returns = self._expiry_returns
    business_days_2_exp = self._business_days_2_expiry
    eom_dates = returns.loc[returns.groupby(returns.index.to_period('M')).apply((lambda x: x.index.max()))].index
    last_month_end = (eom_dates[(- 1)] + pd.offsets.MonthEnd(0))
    eom_dates = eom_dates[:(- 1)]
    eom_dates = eom_dates.insert((- 1), last_month_end)
    roll_dates = eom_dates.sort_values()
    expiry_for_roll = []
    for dts in expiry_dates:
        idx = roll_dates.get_loc(dts, method='ffill')
        expiry_for_roll.append(roll_dates[idx])
    day_diff = (expiry_dates.index - pd.DatetimeIndex(expiry_for_roll))
    front_month_bool = (day_diff.days <= 0)
    back_month_bool = (~ front_month_bool)
    (rolled_return, rolled_future_price) = [pd.concat([item['close2'][back_month_bool], item['close1'][front_month_bool]], axis=0).sort_index() for item in [returns, self.closing_prices]]
    (rolled_expiries, days_2_exp) = [pd.concat([item['expiry2'][back_month_bool], item['expiry1'][front_month_bool]], axis=0).sort_index() for item in [self.expirations, business_days_2_exp]]
    rolled_return[0] = np.nan
    return (rolled_return, rolled_expiries, days_2_exp, rolled_future_price)
