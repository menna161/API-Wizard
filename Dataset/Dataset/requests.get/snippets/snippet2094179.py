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


def get_active_contract(symbol, url=None, n=1):

    def read_cells(row):
        cells = (row.findAll('th') + row.findAll('td'))
        return [cells[0].text.strip(), '', cells[7].text.strip().replace(',', '')]

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
    if (url is None):
        try:
            url = _get_futures_url(symbol, 'quotes_settlements_futures')
        except Exception as e:
            pass
    try:
        c = get_contracts(url)
        if tools.after_third_friday():
            c = c[(c.expiry != datetime.datetime.now().strftime('%Y%m'))]
        if len(c[(c.volume > 100)].index):
            return c.sort_values(by=['volume', 'expiry'], ascending=False)[:n]['expiry'].values[0]
        else:
            return c[:1]['expiry'].values[0]
    except Exception as e:
        if tools.after_third_friday():
            return (datetime.datetime.now() + (datetime.timedelta((365 / 12)) * 2)).strftime('%Y%m')
        else:
            return (datetime.datetime.now() + datetime.timedelta((365 / 12))).strftime('%Y%m')
