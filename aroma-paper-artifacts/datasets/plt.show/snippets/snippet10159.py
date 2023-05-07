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


def plot_grid_multiple(ca_list, shape=None, slice=(- 1), titles=None, colormap='Greys', vmin=None, vmax=None):
    cmap = plt.get_cmap(colormap)
    for i in range(0, len(ca_list)):
        plt.figure(i)
        if (titles is not None):
            plt.title(titles[i])
        activities = list(ca_list[i])
        if (shape is not None):
            activities = np.array(activities).reshape((len(activities), shape[0], shape[1]))[slice]
        plt.imshow(activities, interpolation='none', cmap=cmap, vmin=vmin, vmax=vmax)
    plt.show()
