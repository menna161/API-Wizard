import robin_stocks.robinhood as r
import pandas as pd
import numpy as np
import ta as ta
from pandas.plotting import register_matplotlib_converters
from ta import *
from misc import *
from tradingstats import *
from config import *


def get_modified_holdings():
    " Retrieves the same dictionary as r.build_holdings, but includes data about\n        when the stock was purchased, which is useful for the read_trade_history() method\n        in tradingstats.py\n\n    Returns:\n        the same dict from r.build_holdings, but with an extra key-value pair for each\n        position you have, which is 'bought_at': (the time the stock was purchased)\n    "
    holdings = r.build_holdings()
    holdings_data = r.get_open_stock_positions()
    for (symbol, dict) in holdings.items():
        bought_at = get_position_creation_date(symbol, holdings_data)
        bought_at = str(pd.to_datetime(bought_at))
        holdings[symbol].update({'bought_at': bought_at})
    return holdings
