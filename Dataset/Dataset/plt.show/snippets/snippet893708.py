from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.manifold import TSNE
import numpy as np


def visualize_distribution_time_serie(ts, value, path=None):
    '\n    Visualize the time-serie data in each individual dimensions.\n\n    Parameters\n    ----------\n    ts: numpy array of shape (n_test, n_features)\n        The value of the test time serie data.\n    value: numpy array of shape (n_test, )\n        The outlier score of the test data.\n    path: string\n        The saving path for result figures.\n    '
    sns.set(style='ticks')
    ts = pd.DatetimeIndex(ts)
    value = value.to_numpy()[(:, 1:)]
    data = pd.DataFrame(value, ts)
    data = data.rolling(2).mean()
    sns_plot = sns.lineplot(data=data, palette='BuGn_r', linewidth=0.5)
    if path:
        sns_plot.figure.savefig((path + '/timeserie.png'))
    plt.show()
