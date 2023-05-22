from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime, timezone, timedelta
from decimal import Decimal
import pandas as pd
import requests
import pickle
from .robinhood import Stock, Currency


@staticmethod
def from_robinhood(asset, resolution='1d'):
    'Fetch data from Robinhood\n\n        Args:\n            asset: (Stock or Crypto) A robinhood Stock/Crypto to fetch\n            resolution: (str) The required resolution [15s, 5m, 1d, 1w]\n\n        Returns:\n            (Dataset) with prescribed params and data\n        '
    new_data = defaultdict(dict)
    (interval, span) = {'15s': ('15second', 'hour'), '5m': ('5minute', 'day'), '1d': ('day', 'year'), '1w': ('week', '5year')}[resolution]
    if isinstance(asset, (Currency, Stock)):
        price_data = asset.history(interval=interval, span=span)
        for frame in price_data:
            open_ = frame['open_price']
            high = frame['high_price']
            low = frame['low_price']
            close = frame['close_price']
            volume = frame['volume']
            date = frame['begins_at']
            timestamp = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone(timedelta(0)))
            new_data[timestamp][asset.code] = OHLCV(open_, high, low, close, volume)
        return Dataset(new_data, resolution, [asset.code])
    else:
        raise DatasetException('Invalid asset provided, use robinhood[...].')
