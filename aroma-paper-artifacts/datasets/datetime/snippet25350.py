import datetime
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from ib_insync import Index, Option
from option_utilities import time_it, USSimpleYieldCurve, get_theoretical_strike
from spx_data_update import DividendYieldHistory, IbWrapper
from ib_insync.util import isNan


@staticmethod
def get_option_implied_dividend_yld(qualified_contracts: list, ib, market_price):
    expiration_str = [contract.lastTradeDateOrContractMonth for contract in qualified_contracts]
    timedelta = (pd.DatetimeIndex(expiration_str) - pd.datetime.today())
    year_fraction = (timedelta.days / 365)
    tickers = ib.reqTickers(*qualified_contracts)
    pv_dividends = [ticker.modelGreeks.pvDividend for ticker in tickers]
    dividend_yield = (np.array(pv_dividends) / (market_price * year_fraction))
    return dividend_yield
