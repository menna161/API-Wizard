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


@property
def _expiration_days_2_expiry(self):
    'Returns number of days to expiry for each contract month'
    exp_cols = [col for col in self.raw_tsm_df.columns if ('exp' in col)]
    expiries = self.raw_tsm_df[exp_cols].fillna(0).astype(int).apply(pd.to_datetime, format='%Y%m%d', errors='coerce')
    expiry_list = [expiries[cols].add(pd.Timedelta(days=1)) for cols in expiries.columns]
    num_bus_days = [np.busday_count(item.index.values.astype('<M8[D]'), item.values.astype('<M8[D]')) for item in expiry_list[:(- 1)]]
    num_bus_days = pd.DataFrame(index=expiries.index, data=np.transpose(num_bus_days), columns=expiries.columns[:(- 1)])
    return num_bus_days
