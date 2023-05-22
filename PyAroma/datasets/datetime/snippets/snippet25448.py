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


def get_futures(contract_str, remove_weekly=False):
    ibw = IbWrapper()
    ib = ibw.ib
    vix = Future(contract_str, includeExpired=False)
    cds = ib.reqContractDetails(vix)
    contracts = [cd.contract for cd in cds]
    if remove_weekly:
        contracts = [contract for contract in contracts if (len(contract.localSymbol) <= 4)]
    bars_list = []
    for contract in contracts:
        bars = ib.reqHistoricalData(contract, endDateTime='', durationStr='5 D', barSizeSetting='1 day', whatToShow='TRADES', useRTH=True, formatDate=1)
        if bars:
            bars_list.append(util.df(bars))
    ib.disconnect()
    contract_df = util.df(contracts)
    close_list = [item.loc[(:, ['date', 'close'])] for item in bars_list]
    close_list = [item.set_index('date') for item in close_list]
    close_list = [item.rename(index=str, columns={'close': name}) for (item, name) in zip(close_list, pd.to_datetime(contract_df['lastTradeDateOrContractMonth']))]
    future_series = pd.concat(close_list, axis=1, sort=False)
    future_series = future_series.transpose().sort_index()
    future_series.columns = pd.to_datetime(future_series.columns)
    return (future_series, contract_df)
