from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
import random
import time
from .dataset import RESOLUTIONS


def log_as_dataframe(self):
    'Convert log to a pandas DataFrame\n\n        Returns:\n            (DataFrame)\n        '
    df = pd.DataFrame.from_dict(self.log).set_index('datetime')
    df.index = pd.to_datetime(df.index)
    numeric_cols = ['start_cash', 'end_cash', 'start_portfolio_value', 'end_portfolio_value']
    for symbol in self.symbols:
        numeric_cols.append(('start_owned_' + symbol))
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric)
    return df
