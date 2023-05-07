from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
import random
import time
from .dataset import RESOLUTIONS


def plot_assets(self, symbols=None, ax=None, show=False):
    'Plot assets\n\n        Args:\n            symbols: (list: str) the symbols to include, defaults to all\n            ax: (Axis) where to plot, defaults to pandas\n            show: (bool) display the plot\n        '
    if (not symbols):
        symbols = self.symbols
    df = self.log_as_dataframe()
    df[[('end_owned_' + symbol) for symbol in self.symbols]].plot(ax=ax)
    if show:
        plt.show()
