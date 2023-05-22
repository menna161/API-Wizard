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


def get_vix():
    "Fetch vix from Interactive Brokers and append to history'''\n    :return: Dataframe\n    "
    ibw = IbWrapper()
    ib = ibw.ib
    vix = Index('VIX')
    cds = ib.reqContractDetails(vix)
    bars = ib.reqHistoricalData(cds[0].contract, endDateTime='', durationStr='1 Y', barSizeSetting='1 day', whatToShow='TRADES', useRTH=True, formatDate=1)
    ib.disconnect()
    vix = util.df(bars)
    vix = vix.set_index('date')
    vix.index = pd.to_datetime(vix.index)
    vix = vix[['open', 'high', 'low', 'close']]
    vix_history = read_feather(str((UpdateSP500Data.TOP_LEVEL_PATH / 'vix_history')))
    full_hist = vix.combine_first(vix_history)
    write_feather(full_hist, str((UpdateSP500Data.TOP_LEVEL_PATH / 'vix_history')))
    return full_hist['close']
