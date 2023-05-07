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


def plot_grid(activities, shape=None, slice=(- 1), title='', colormap='Greys', vmin=None, vmax=None, node_annotations=None, show_grid=False):
    if (shape is not None):
        activities = np.array(activities).reshape((len(activities), shape[0], shape[1]))[slice]
    cmap = plt.get_cmap(colormap)
    plt.title(title)
    plt.imshow(activities, interpolation='none', cmap=cmap, vmin=vmin, vmax=vmax)
    if (node_annotations is not None):
        for i in range(len(node_annotations)):
            for j in range(len(node_annotations[i])):
                plt.text(j, i, node_annotations[i][j], ha='center', va='center', color='grey', fontdict={'weight': 'bold', 'size': 6})
    if show_grid:
        plt.grid(which='major', axis='both', linestyle='-', color='grey', linewidth=0.5)
        plt.xticks(np.arange((- 0.5), len(activities[0]), 1), '')
        plt.yticks(np.arange((- 0.5), len(activities), 1), '')
        plt.tick_params(axis='both', which='both', length=0)
    plt.show()
