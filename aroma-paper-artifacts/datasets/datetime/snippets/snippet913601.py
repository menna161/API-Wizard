from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime, timezone, timedelta
from decimal import Decimal
import pandas as pd
import requests
import pickle
from .robinhood import Stock, Currency


@staticmethod
def from_alphavantage(symbol, resolution='1d', api_key='demo'):
    'Fetch data from AlphaVantage\n\n        Args:\n            symbol: (str) Stock to Fetch\n            resolution: (str) The required resolution [5m, 1d]\n            api_key: (str) Your API key\n        Returns:\n            (Dataset) with prescribed params and data\n        '
    assert (resolution in ['1d', '5m'])
    url = 'https://www.alphavantage.co/query?outputsize=full&symbol={}&apikey={}'.format(symbol, api_key)
    if (resolution == '1d'):
        url += '&function=TIME_SERIES_DAILY'
        data_key = 'Time Series (Daily)'
        time_format = '%Y-%m-%d'
    else:
        url += '&function=TIME_SERIES_INTRADAY&interval=5min'
        data_key = 'Time Series (5min)'
        time_format = '%Y-%m-%d %H:%M:%S'
    res = requests.get(url).json()
    new_data = defaultdict(dict)
    for timestamp in res[data_key]:
        date = datetime.strptime(timestamp, time_format)
        tick_data = res[data_key][timestamp]
        price_data = OHLCV(tick_data['1. open'], tick_data['2. high'], tick_data['3. low'], tick_data['4. close'], tick_data['5. volume'])
        new_data[date][symbol] = price_data
    if (len(new_data) == 0):
        raise DatasetException('No data')
    return Dataset(new_data, resolution, [symbol])
