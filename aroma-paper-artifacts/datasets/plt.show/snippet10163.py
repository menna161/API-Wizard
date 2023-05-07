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


def plot_network(network, layout='shell', with_labels=True, node_color='#1f78b4', node_size=300):
    G = network.to_networkx()
    if (layout == 'shell'):
        nx.draw_shell(G, with_labels=with_labels, node_color=node_color, node_size=node_size)
    elif (layout == 'spring'):
        nx.draw_spring(G, with_labels=with_labels, node_color=node_color, node_size=node_size)
    elif isinstance(layout, dict):
        nx.draw(G, pos=layout, with_labels=with_labels, node_color=node_color, node_size=node_size)
    else:
        raise Exception(('unsupported layout: %s' % layout))
    plt.show()
