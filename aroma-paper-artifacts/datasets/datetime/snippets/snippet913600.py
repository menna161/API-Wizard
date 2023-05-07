from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime, timezone, timedelta
from decimal import Decimal
import pandas as pd
import requests
import pickle
from .robinhood import Stock, Currency


@staticmethod
def from_google(symbol, resolution='1d', period='20d', exchange='NASD'):
    'Fetch data from google\n\n        Args:\n            symbol: (str) Stock to Fetch\n            resolution: (str) The required resolution\n                which must be a key of `RESOLUTIONS`\n            period: (str) The amount of time to fetch, note:\n                google will automatically limit this\n            exchange: (str) The stock exchange\n\n        Returns:\n            (Dataset) with prescribed params and data\n\n        Note:\n            No longer supported by Google.\n        '
    interval = RESOLUTIONS[resolution]
    url = f'https://www.google.com/finance/getprices?i={interval}&p={period}&f=d,o,h,l,c,v&df=cpct&q={symbol}&x={exchange}'
    res = requests.get(url).text
    lines = res.split('\n')[7:]
    ref_date = None
    new_data = defaultdict(dict)
    for line in lines:
        if ((not line) or ('=' in line)):
            continue
        (date, close, high, low, open_, volume) = line.split(',')
        if date.startswith('a'):
            date = int(date[1:])
            ref_date = date
        else:
            date = (ref_date + (interval * int(date)))
        timestamp = datetime.fromtimestamp(date).isoformat()
        new_data[timestamp][symbol] = OHLCV(open_, high, low, close, volume)
    if (len(new_data) == 0):
        raise DatasetException('No data')
    return Dataset(new_data, resolution, [symbol])
