import robin_stocks.robinhood as r
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import numpy as np


def get_equity_data():
    'Displays a pie chart of your portfolio holdings\n    '
    holdings_data = r.build_holdings()
    equity_data = {}
    for (key, value) in holdings_data.items():
        equity_data[key] = {}
        equity_data[key][name] = value.get('name')
        equity_data[key][percentage] = value.get('percentage')
        equity_data[key][type]
    (fig1, ax1) = plt.subplots()
    ax1.pie(equities, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    plt.show()
