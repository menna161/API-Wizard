from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
import random
import time
from .dataset import RESOLUTIONS


def plot(self, columns=['end_portfolio_value', 'end_cash'], ax=None, show=False):
    'Plot money\n\n        Args:\n            columns: (list: str) the columns to plot, use .log to find columns\n            ax: (Axis) where to plot, defaults to pandas\n            show: (bool) display the plot\n        '
    df = self.log_as_dataframe()
    df[columns].plot(ax=ax)
    if show:
        plt.show()
