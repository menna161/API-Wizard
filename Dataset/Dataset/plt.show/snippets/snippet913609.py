from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime, timezone, timedelta
from decimal import Decimal
import pandas as pd
import requests
import pickle
from .robinhood import Stock, Currency


def plot(self, columns=['close'], symbols=None, ax=None, show=False):
    'Plot\n\n        Args:\n            columns: (list: str) Columns to plot,\n                [open, high, low, close, relclose, relprevclose, volume]\n            symbols: (list: str) Symbols to include,\n                defaults to all in dataset\n            ax: (Axes) Where to plot, defaults to pandas default\n            show: (bool) Whether to run plt.show()\n        '
    if (not symbols):
        symbols = self.symbols
    filter_ = [((col + '_') + symbol) for col in columns for symbol in symbols]
    df = self.as_dataframe(symbols)[filter_].plot(ax=ax, title=str(self))
    if show:
        plt.show()
