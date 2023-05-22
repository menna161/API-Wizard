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


def bifurcation_plot(x, trajectories, timesteps, xlabel=None, ylabel=None, title=None):
    '\n    Create a bifurcation plot.\n\n    :param x: A list representing the values of the x-axis.\n\n    :param trajectories: A list of lists. Each inner list is a sequence of activities representing a trajectory.\n\n    :param timesteps: The number of timesteps in the trajectory to consider, starting from the end.\n\n    :param xlabel: A string representing the label of the x-axis.\n\n    :param ylabel: A string representing the label of the y-axis.\n\n    :param title: The plot title.\n    '
    y = []
    for t in trajectories:
        y.append(np.unique(t[(- timesteps):]))
    for (x_e, y_e) in zip(x, y):
        plt.scatter(([x_e] * len(y_e)), y_e, color='b', s=1)
    if xlabel:
        plt.xlabel(xlabel)
    if ylabel:
        plt.ylabel(ylabel)
    if title:
        plt.title(title)
    plt.show()
