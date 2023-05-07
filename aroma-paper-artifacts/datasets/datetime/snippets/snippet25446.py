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


def __init__(self):
    db_directory = (UpdateSP500Data.DATA_BASE_PATH / 'xl')
    cboe_dict = {'cboe_vvix': 'http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/vvixtimeseries.csv', 'cboe_skew': 'http://www.cboe.com/publish/scheduledtask/mktdata/datahouse/skewdailyprices.csv'}
    [urlretrieve(value, (db_directory / str((key + '.csv')))) for (key, value) in cboe_dict.items()]
    (vvix, skew) = [pd.read_csv(value, str((db_directory / str((key + '.csv')))), skiprows=1, delimiter=',') for (key, value) in cboe_dict.items()]
    (vvix['Date'], skew['Date']) = [df['Date'].apply(pd.to_datetime) for df in [vvix, skew]]
    (vvix, skew) = [df.set_index('Date') for df in [vvix, skew]]
    (vvix, skew) = [item[item.columns[0]] for item in [vvix, skew]]
    (self.vvix, self.skew) = [item.ffill() for item in [vvix, skew]]
