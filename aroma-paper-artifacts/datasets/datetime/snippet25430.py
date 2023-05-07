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


def csv2feather(self, in_directory, out_directory, archive_files=True):
    'Open raw csv files, remove weekly options and all options not in\n        root_symbols_file build dataframe and convert to feather\n        archive zip and csv files'
    zip_archive_directory = (self.top_level_directory / 'zip')
    csv_archive_directory = (self.top_level_directory / 'csv')
    if (not os.path.isdir(out_directory)):
        os.mkdir(out_directory)
    regex_pattern = '|'.join(self.root_symbols_str)
    for item in os.listdir(in_directory):
        if item.endswith('.csv'):
            option_df = pd.read_csv((in_directory / item))
            option_df[['quote_date', 'expiration']] = option_df[['quote_date', 'expiration']].apply(pd.to_datetime)
            option_df['option_type'] = option_df['option_type'].apply(str.upper)
            option_df = option_df[(~ option_df['root'].str.contains('SPXW'))]
            option_df = option_df[option_df['root'].str.contains(regex_pattern)]
            for option_type in self.OPTION_TYPES:
                df2save = option_df[(option_df['option_type'] == option_type)]
                file_name = (((os.path.splitext(item)[0] + '_') + option_type) + '.feather')
                df2save.reset_index().to_feather(str((out_directory / file_name)))
    if archive_files:
        for item in os.listdir(in_directory):
            if item.endswith('.csv'):
                os.rename((in_directory / item), str((csv_archive_directory / item)))
            elif item.endswith('.zip'):
                os.rename((in_directory / item), str((zip_archive_directory / item)))
            else:
                os.remove((in_directory / item))
