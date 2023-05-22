import robin_stocks.robinhood as r
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np


def show_plot(price, firstIndicator, secondIndicator, dates, symbol='', label1='', label2=''):
    "Displays a chart of the price and indicators for a stock\n\n    Args:\n        price(Pandas series): Series containing a stock's prices\n        firstIndicator(Pandas series): Series containing a technical indicator, such as 50-day moving average\n        secondIndicator(Pandas series): Series containing a technical indicator, such as 200-day moving average\n        dates(Pandas series): Series containing the dates that correspond to the prices and indicators\n        label1(str): Chart label of the first technical indicator\n        label2(str): Chart label of the first technical indicator\n\n    Returns:\n        True if the stock's current price is higher than it was five years ago, or the stock IPO'd within the last five years\n        False otherwise\n    "
    plt.figure(figsize=(10, 5))
    plt.title(symbol)
    plt.plot(dates, price, label='Closing prices')
    plt.plot(dates, firstIndicator, label=label1)
    plt.plot(dates, secondIndicator, label=label2)
    plt.yticks(np.arange(price.min(), price.max(), step=((price.max() - price.min()) / 15.0)))
    plt.legend()
    plt.show()
