import torch
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from torchvision.utils import make_grid


def plot_line(x, xp_path, filename, title='', xlabel='Epochs', ylabel='Values', legendlabel=None, log_scale=False):
    '\n    Draw a line plot with grouping options.\n\n    :param x: Data as a series, 1d-array, or list.\n    :param xp_path: Export path for the plot as string.\n    :param filename: Filename as string.\n    :param title: Title for the plot as string. Optional.\n    :param xlabel: Label for x-axis as string. Optional.\n    :param ylabel: Label for y-axis as string. Optional.\n    :param legendlabel: String or list of strings with data series legend labels. Optional.\n    :param log_scale: Boolean to set y-axis to log-scale.\n    '
    sns.set()
    sns.set_style('whitegrid')
    data = {'x': [], 'y': [], 'label': []}
    if isinstance(x, list):
        n_series = len(x)
        if (legendlabel is None):
            legendlabel = [('series ' + str((i + 1))) for i in range(n_series)]
        else:
            assert (len(legendlabel) == n_series)
        for (i, series) in enumerate(x):
            data['x'].extend(list(range(1, (len(x[i]) + 1))))
            data['y'].extend(list(x[i]))
            data['label'].extend(([legendlabel[i]] * len(x[i])))
    else:
        if (legendlabel is None):
            legendlabel = ['series 1']
        else:
            assert (len(legendlabel) == 1)
        data['x'].extend(list(range(1, (len(x) + 1))))
        data['y'].extend(list(x))
        data['label'].extend((legendlabel * len(x)))
    df = pd.DataFrame(data, columns=['x', 'y', 'label'])
    sns.lineplot(x='x', y='y', hue='label', data=df, palette='colorblind')
    if log_scale:
        plt.yscale('symlog')
        plt.grid(True, axis='both')
    else:
        plt.grid(False, axis='x')
        plt.grid(True, axis='y')
    if (not (title == '')):
        plt.title(title)
    plt.legend(legendlabel, title=False)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(((xp_path + '/') + filename), bbox_inches='tight')
    plt.clf()
