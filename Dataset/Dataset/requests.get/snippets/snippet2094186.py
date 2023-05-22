import datetime
import os.path
import pandas as pd
import numpy as np
import re
import time
import tempfile
import sys
import requests
from bs4 import BeautifulSoup as bs
from dateutil.parser import parse as parse_date
from qtpylib import tools
import logging


def get_contracts(url):
    html = requests.get(url, timeout=5)
    html = bs(html.text, 'html.parser')
    ' CME switched to using ajax '
    prodDataUrl = html.text.split('component.baseUrl = "')[1].split(';')[0].replace('" + ', '').replace(' + "', '').strip('"')
    url = ('https://www.cmegroup.com%s?tradeDate=%s' % (prodDataUrl, datetime.datetime.now().strftime('%m/%d/%Y')))
    data = requests.get(url, timeout=5).json()
    if (len(data['settlements']) == 1):
        url = ('https://www.cmegroup.com%s?tradeDate=%s' % (prodDataUrl, parse_date(data['updateTime']).strftime('%m/%d/%Y')))
        data = requests.get(url, timeout=5).json()
    df = pd.DataFrame(data['settlements'])[:(- 1)][['month', 'volume']]
    df.columns = ['expiry', 'volume']
    df.volume = pd.to_numeric(df.volume.str.replace(',', ''))
    df.expiry = df.expiry.str.replace('JLY', 'JUL').apply((lambda ds: parse_date(ds).strftime('%Y%m')))
    try:
        df = df.reset_index().drop_duplicates(keep='last')
    except Exception as e:
        df = df.reset_index().drop_duplicates(take_last=True)
    return df[:13].dropna()
