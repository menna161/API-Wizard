from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime, timezone, timedelta
from decimal import Decimal
import pandas as pd
import requests
import pickle
from .robinhood import Stock, Currency


def as_dataframe(self, symbols=None):
    'Convert to dataframe\n\n        Args:\n            symbols: (list: str) Symbols to include,\n                will default to all in dataset\n\n        Returns:\n            (Dataframe) with data from dataset\n        '
    if (not symbols):
        symbols = self.symbols
    data = defaultdict(list)
    data['datetime'] = self.dates
    for symbol in symbols:
        init_close = self.data[data['datetime'][0]][symbol].close
        prev_close = init_close
        for timestamp in data['datetime']:
            price_data = self.data[timestamp][symbol]
            data[('open_' + symbol)].append(price_data.open)
            data[('high_' + symbol)].append(price_data.high)
            data[('low_' + symbol)].append(price_data.low)
            data[('close_' + symbol)].append(price_data.close)
            data[('relclose_' + symbol)].append((price_data.close / init_close))
            data[('relprevclose_' + symbol)].append((price_data.close / prev_close))
            data[('volume_' + symbol)].append(price_data.volume)
            prev_close = price_data.close
    df = pd.DataFrame.from_dict(data).set_index('datetime')
    df.index = pd.to_datetime(df.index)
    return df
