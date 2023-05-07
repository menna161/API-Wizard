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


@property
def _business_days_2_expiry(self):
    ' Returns number of business days to expiration '
    expirations = self.expirations.copy()
    column_names = self.expirations.columns
    business_day_list = []
    _notNaT = np.datetime64(pd.datetime.today())
    for col in column_names:
        expiry = expirations[col]
        begin_dates = expiry.index
        end_dates = pd.DatetimeIndex(expiry.values)
        end_dates_mask = end_dates.to_series().isna().values
        bus_days = np.busday_count(list(begin_dates.date), list(pd.DatetimeIndex(np.where(end_dates_mask, _notNaT, end_dates)).date))
        out_bus_days = [(np.nan if (x in bus_days[end_dates_mask]) else x) for x in bus_days]
        business_day_list.append(pd.Series(data=out_bus_days, index=expiry.index, name=col))
    return pd.concat(business_day_list, axis=1)
