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


def update_data_files(self, temporary_file_directory):
    ' Download zip files from CBOE, unzip to csv, process and turn into feather\n        TODO: Should be in separate simulation data update & fetch class that creates/updates database\n         :rtype: Bool'
    feather_directory = (self.top_level_directory / 'feather')
    assert feather_directory.is_dir()
    assert temporary_file_directory.is_dir(), '{} directory does not exist'.format(temporary_file_directory)
    latest_business_date = (pd.to_datetime('today') - pd.tseries.offsets.BDay(1))
    opt_dates_all = get_dates(feather_directory)
    if (opt_dates_all[(- 1)].date() != latest_business_date.date()):
        start_time = time()
        print('Downloading Option data from CBOE')
        self.get_subscription_files(temporary_file_directory)
        self.unzip_file(temporary_file_directory, temporary_file_directory)
        self.csv2feather(temporary_file_directory, feather_directory)
        end_time = time()
        files_updated = True
        print((('Option files updated in: ' + str(round((end_time - start_time)))) + ' seconds'))
    else:
        files_updated = False
        print('Option files not updated')
    return files_updated
