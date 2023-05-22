import robin_stocks.robinhood as r
import pandas as pd
import numpy as np
import ta as ta
from pandas.plotting import register_matplotlib_converters
from ta import *
from misc import *
from tradingstats import *
from config import *


def five_year_check(stockTicker):
    "Figure out if a stock has risen or been created within the last five years.\n\n    Args:\n        stockTicker(str): Symbol of the stock we're querying\n\n    Returns:\n        True if the stock's current price is higher than it was five years ago, or the stock IPO'd within the last five years\n        False otherwise\n    "
    instrument = r.get_instruments_by_symbols(stockTicker)
    if ((instrument is None) or (len(instrument) == 0)):
        return True
    list_date = instrument[0].get('list_date')
    if ((pd.Timestamp('now') - pd.to_datetime(list_date)) < pd.Timedelta('5 Y')):
        return True
    fiveyear = get_historicals(stockTicker, 'day', '5year', 'regular')
    if ((fiveyear is None) or (None in fiveyear)):
        return True
    closingPrices = []
    for item in fiveyear:
        closingPrices.append(float(item['close_price']))
    recent_price = closingPrices[(len(closingPrices) - 1)]
    oldest_price = closingPrices[0]
    return (recent_price > oldest_price)
