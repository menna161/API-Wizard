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


def poincare_plot(activities, timesteps, xlabel=None, ylabel=None, xlim=None, ylim=None, title=None):
    '\n    Create a Poincaré plot.\n\n    :param activities: A list of activities. If the values of this list are also lists, then each will\n                       be plotted as a separate series.\n\n    :param timesteps: The number of timesteps in the trajectory to consider, starting from the end.\n\n    :param xlabel: A string representing the label of the x-axis.\n\n    :param ylabel: A string representing the label of the y-axis.\n\n    :param xlim: A 2-tuple of numbers, representing the limits of the x-axis.\n\n    :param ylim: A 2-tuple of numbers, or a list of at most two 2-tuples of numbers, representing the\n                 limits of the y-axis.\n\n    :param title: The plot title.\n    '
    cm = plt.get_cmap('gist_rainbow')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    is_multiseries = isinstance(activities[0], (list, np.ndarray))
    if is_multiseries:
        ax.set_prop_cycle(color=[cm(((1.0 * i) / len(activities))) for i in range(len(activities))])
    else:
        activities = [activities]
    for a in activities:
        x = []
        y = []
        for t in range((timesteps - 1)):
            x.append(a[(- timesteps):][t])
            y.append(a[(- timesteps):][(t + 1)])
        plt.scatter(x, y, s=1)
    if xlim:
        plt.xlim(xlim)
    if ylim:
        plt.ylim(ylim)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    if title:
        plt.title(title)
    plt.show()
