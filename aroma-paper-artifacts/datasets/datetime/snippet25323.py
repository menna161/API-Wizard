import datetime
import pandas as pd
import numpy as np
from abc import ABC, abstractmethod
from ib_insync import Index, Option
from option_utilities import time_it, USSimpleYieldCurve, get_theoretical_strike
from spx_data_update import DividendYieldHistory, IbWrapper
from ib_insync.util import isNan


@property
def get_expirations(self):
    'Retrieve Dataframe of option expirations (last trading day) for option chain in object'
    expirations = pd.DataFrame(list(self.chain.expirations), index=pd.DatetimeIndex(self.chain.expirations), columns=['expirations'])
    timedelta = (expirations.index - datetime.datetime.today())
    expirations['year_fraction'] = (timedelta.days / 365)
    expirations = expirations[(expirations['year_fraction'] > 0)]
    return expirations.sort_index()
