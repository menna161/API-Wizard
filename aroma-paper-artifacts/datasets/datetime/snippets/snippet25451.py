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
def vix_history(self):
    iv_hist = ImpliedVolatilityHistory()
    vix = iv_hist.implied_vol_index
    if (vix.index[(- 1)].date() == pd.to_datetime('today').date()):
        vix = vix[:(- 1)]
    return vix
