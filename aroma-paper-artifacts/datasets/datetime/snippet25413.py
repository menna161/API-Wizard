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


def scrape_sp5_div_yield():
    'Scrape S&P 500 dividend yield from www.multpl.com\n    :rtype: pd.Dataframe\n    '
    url = 'http://www.multpl.com/s-p-500-dividend-yield/table?f=m'
    raw_html_tbl = pd.read_html(url)
    dy_df = raw_html_tbl[0]
    dy_df.columns = dy_df.iloc[0]
    dy_df = dy_df.drop([0])
    dy_df[dy_df.columns[0]] = pd.to_datetime(dy_df.loc[(:, dy_df.columns[0])], format='%b %d, %Y')
    dy_df = dy_df.set_index(dy_df.columns[0])
    dy_df = dy_df[dy_df.columns[0]]
    spx_dividend_yld = pd.to_numeric(dy_df.str.replace('%', '').str.replace('estimate', '').str.strip())
    spx_dividend_yld = spx_dividend_yld.reindex(spx_dividend_yld.index[::(- 1)])
    spx_dividend_yld = spx_dividend_yld.resample('MS').bfill()
    return spx_dividend_yld
