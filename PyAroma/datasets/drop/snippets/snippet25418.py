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


def feather_clean(in_directory):
    ' Utility function to clean feather files'
    Path.is_dir(in_directory)
    all_files = os.listdir(in_directory)
    for item in all_files:
        if item.endswith('.feather'):
            option_df = pd.read_feather((in_directory / item))
            idx = (option_df['strike'] == 5)
            option_df = option_df.drop(option_df.index[idx])
            option_df.to_feather(str((in_directory / item)))
