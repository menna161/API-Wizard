from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime, timezone, timedelta
from decimal import Decimal
import pandas as pd
import requests
import pickle
from .robinhood import Stock, Currency


@staticmethod
def from_cryptocompare(symbol, resolution='1d', to_symbol='USD', limit=3000, last_unix_time=None):
    'Fetch data from cryptocompare\n\n        Args:\n            symbol: (str) Stock to Fetch\n            resolution: (str) The required resolution\n                which must be a key of `RESOLUTIONS`\n            to_symbol: (str) The unit to convert symbol data to,\n                this can be a currency or crypto\n            limit: (int) limit the num of datapoints returned\n            last_unix_time: (int) Specify the last timestep of the query\n\n        Returns:\n            (Dataset) with prescribed params and data\n        '
    endpoints = {'1d': 'histoday', '1h': 'histohour', '1m': 'histominute'}
    url = f'https://min-api.cryptocompare.com/data/{endpoints[resolution]}?fsym={symbol}&tsym={to_symbol}&limit={limit}'
    if last_unix_time:
        url += f'&{last_unix_time}'
    res = requests.get(url).json()
    new_data = defaultdict(dict)
    for data in res['Data']:
        open_ = data['open']
        high = data['high']
        low = data['low']
        close = data['close']
        volume = data['volumefrom']
        timestamp = datetime.fromtimestamp(data['time']).isoformat()
        new_data[timestamp][symbol] = OHLCV(open_, high, low, close, volume)
    if (len(new_data) == 0):
        raise DatasetException('No data')
    return Dataset(new_data, resolution, [symbol])
