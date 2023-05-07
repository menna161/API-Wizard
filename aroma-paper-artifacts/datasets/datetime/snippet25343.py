import datetime
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from ib_insync import Index, Option
from option_utilities import time_it, USSimpleYieldCurve, get_theoretical_strike
from spx_data_update import DividendYieldHistory, IbWrapper
from ib_insync.util import isNan


def __init__(self, opt_asset: OptionAsset):
    self.option_asset = opt_asset
    self.trade_date = pd.DatetimeIndex([datetime.datetime.today()], tz='US/Eastern')
    self.zero_curve = USSimpleYieldCurve()
    self.dividend_yield = self.option_asset.get_dividend_yield()
    self.option_expiry = None
