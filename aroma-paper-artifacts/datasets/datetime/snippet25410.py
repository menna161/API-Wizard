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


def get_dates(feather_directory, file_type='.feather'):
    ' Fetch dates from feather file names\n    :rtype: pd.DatetimeIndex\n    '
    regex_pattern = '\\d{4}-\\d{2}-\\d{2}'
    opt_dates_list = []
    for item in os.listdir(feather_directory):
        if item.endswith(file_type):
            date_string = re.search(regex_pattern, item)
            if date_string:
                opt_dates_list.append(date_string.group())
    opt_dates_list = list(set(opt_dates_list))
    opt_dates_all = pd.DatetimeIndex([pd.to_datetime(date_item, yearfirst=True, format='%Y-%m-%d') for date_item in opt_dates_list])
    opt_dates_all = opt_dates_all.sort_values()
    return opt_dates_all
