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


def __init__(self, expiry_type=0):
    ' Class to retrieve tsm vix futures data and create return and index series'
    try:
        raw_tsm = loadmat('/Volumes/ExtraStorage/base/db/fut/vix.mat')
    except FileNotFoundError:
        raw_tsm = loadmat(str(((UpdateSP500Data.DATA_BASE_PATH / 'mat') / 'vix.mat')))
    python_dates = matlab2datetime(raw_tsm['t'].squeeze())
    column_names = [item[0] for item in raw_tsm['h'][(:, 0)]]
    raw_x_data = np.round(raw_tsm['x'], 4)
    self.raw_tsm_df = pd.DataFrame(data=raw_x_data, index=python_dates, columns=column_names)
    self.raw_tsm_df = self.raw_tsm_df.iloc[(:(- 1), :)]
    self.start_date = self.raw_tsm_df.index[0]
    self.expiry_type = expiry_type
    (self.rolled_return, self.rolled_expiries, self.days_2_exp, self.rolled_future) = self._rolled_future_return()
