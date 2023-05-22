import networkx as nx
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.collections as mcoll
import collections
from .state import State
from .substitution_system import SubstitutionSystem
import cPickle as pickle
import pickle


def plot1D(x, y, color=None, label=None, xlabel=None, ylabel=None, xlim=None, ylim=None, twinx=False, legend=None, tight_layout=None, title=None):
    '\n    Creates a 1D plot of the given x and y values.\n\n    :param x: A list representing the values of the x-axis.\n\n    :param y: A list representing the values of the y-axis. If the values of this list are also lists, then each will\n              be plotted as a separate series on the y-axis.\n\n    :param color: A string, representing the color of the series, or a list of colors, representing the color of each\n                   series to be plotted. The number of colors must match the number of series. The color values must\n                   be recognizable by Matplotlib.\n\n    :param label: A string or number, or a list of strings or numbers, representing the labels of each series to be\n                  plotted. The number of labels must match the number of series.\n\n    :param xlabel: A string representing the label of the x-axis.\n\n    :param ylabel: A string, or list of at most two strings, representing the label(s) of the y-axis.\n\n    :param xlim: A 2-tuple of numbers, representing the limits of the x-axis.\n\n    :param ylim: A 2-tuple of numbers, or a list of at most two 2-tuples of numbers, representing the\n                 limits of the y-axis.\n\n    :param twinx: If True, the provided y series will be plotted on two separate y-axes, and there must\n                  be at least two series of y values provided. If there are more than two series of y values,\n                  then each series will be plotted on alternating y-axes. (Default is False)\n\n    :param legend: A dict, or a list of at most two dicts, representing the arguments to the legend\n                   function of Matplotlib.\n\n    :param tight_layout: A dict representing the arguments to the tight_layout function of Matplotlib.\n\n    :param title: The plot title.\n    '
    axes = []
    (fig, ax1) = plt.subplots()
    axes.append(ax1)
    if twinx:
        axes.append(ax1.twinx())
        if (len(y) < 2):
            raise Exception('there must be at least two series of y values provided')
        for _y in y:
            if (not isinstance(_y, (list, np.ndarray))):
                raise Exception('an item in y must be a list representing a y series')
    current_axis_idx = 0
    is_multiseries = isinstance(y[0], (list, np.ndarray))

    def _get_item(items, i):
        if isinstance(items, str):
            return items
        if isinstance(items, collections.Sequence):
            return items[i]
        return items
    if (not is_multiseries):
        y = [y]
    for (i, y_series) in enumerate(y):
        current_axis = axes[(current_axis_idx % len(axes))]
        plot_args = {}
        if label:
            plot_args['label'] = _get_item(label, i)
        if color:
            plot_args['color'] = _get_item(color, i)
        current_axis.plot(x, y_series, **plot_args)
        if xlabel:
            current_axis.set_xlabel(xlabel)
        if ylabel:
            ylabel_args = {}
            if color:
                ylabel_args['color'] = _get_item(color, i)
            current_axis.set_ylabel(_get_item(ylabel, (i % 2)), **ylabel_args)
        if xlim:
            current_axis.set_xlim(xlim)
        if ylim:
            current_axis.set_ylim(_get_item(ylim, (i % 2)))
        if legend:
            current_axis.legend(**legend)
        current_axis_idx += 1
    if tight_layout:
        plt.tight_layout(**tight_layout)
    if title:
        plt.title(title)
    plt.show()
