from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
import random
import time
from .dataset import RESOLUTIONS


def _step(self, current_date, *args, **kwargs):
    'Run algo one timestep\n\n        This is an internal method used by classes which implement BaseTraderself.\n        Do not call with algorithm.\n        '
    self.log['datetime'].append(current_date)
    self.log['start_cash'].append(self.cash)
    self.log['start_portfolio_value'].append(self.portfolio_value)
    for symbol in self.symbols:
        self.log[('start_owned_' + symbol)].append(self.quantity(symbol))
        self.log[('start_price_' + symbol)].append(self.price(symbol))
    self.loop(current_date, *args, **kwargs)
    self.log['end_cash'].append(self.cash)
    self.log['end_portfolio_value'].append(self.portfolio_value)
    for symbol in self.symbols:
        self.log[('end_owned_' + symbol)].append(self.quantity(symbol))
        self.log[('end_price_' + symbol)].append(self.price(symbol))
