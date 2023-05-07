import robin_stocks.robinhood as r
import pandas as pd
import numpy as np
import ta as ta
from pandas.plotting import register_matplotlib_converters
from ta import *
from misc import *
from tradingstats import *
from config import *


def golden_cross(stockTicker, n1, n2, days, direction=''):
    'Determine if a golden/death cross has occured for a specified stock in the last X trading days\n\n    Args:\n        stockTicker(str): Symbol of the stock we\'re querying\n        n1(int): Specifies the short-term indicator as an X-day moving average.\n        n2(int): Specifies the long-term indicator as an X-day moving average.\n                 (n1 should be smaller than n2 to produce meaningful results, e.g n1=50, n2=200)\n        days(int): Specifies the maximum number of days that the cross can occur by\n        direction(str): "above" if we are searching for an upwards cross, "below" if we are searching for a downwaords cross. Optional, used for printing purposes\n\n    Returns:\n        1 if the short-term indicator crosses above the long-term one\n        0 if there is no cross between the indicators\n        -1 if the short-term indicator crosses below the long-term one\n        False if direction == "above" and five_year_check(stockTicker) returns False, meaning that we\'re considering whether to\n            buy the stock but it hasn\'t risen overall in the last five years, suggesting it contains fundamental issues\n    '
    if ((direction == 'above') and (not five_year_check(stockTicker))):
        return False
    history = get_historicals(stockTicker, 'day', 'year', 'regular')
    if ((history is None) or (None in history)):
        return False
    closingPrices = []
    dates = []
    for item in history:
        closingPrices.append(float(item['close_price']))
        dates.append(item['begins_at'])
    price = pd.Series(closingPrices)
    dates = pd.Series(dates)
    dates = pd.to_datetime(dates)
    sma1 = ta.volatility.bollinger_mavg(price, int(n1), False)
    sma2 = ta.volatility.bollinger_mavg(price, int(n2), False)
    series = [price.rename('Price'), sma1.rename('Indicator1'), sma2.rename('Indicator2'), dates.rename('Dates')]
    df = pd.concat(series, axis=1)
    cross = get_last_crossing(df, days, symbol=stockTicker, direction=direction)
    if (cross and plot):
        show_plot(price, sma1, sma2, dates, symbol=stockTicker, label1=(str(n1) + ' day SMA'), label2=(str(n2) + ' day SMA'))
    return cross
