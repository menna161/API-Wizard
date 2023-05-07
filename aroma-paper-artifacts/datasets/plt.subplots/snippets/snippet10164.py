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


def animate_network(trajectory, save=False, interval=50, dpi=80, layout='shell', with_labels=True, with_arrows=True, node_color='b', node_size=30, with_timestep=False, show=True):
    (fig, ax) = plt.subplots()

    def update(arg):
        ax.clear()
        (i, state) = arg
        if with_timestep:
            ax.set_title(('timestep: %s' % (i + 1)))
        color = (node_color[i] if (type(node_color) == dict) else node_color)
        network = state.network
        G = nx.MultiDiGraph()
        for n in network.nodes:
            G.add_node(n)
        for edge in network.edges:
            G.add_edge(edge[0], edge[1])
        state_layout = (layout[i] if ((type(layout) == list) or (type(layout) == tuple)) else layout)
        if (state_layout == 'shell'):
            nx.draw_shell(G, with_labels=with_labels, node_color=color, node_size=node_size, arrows=with_arrows)
        elif (state_layout == 'spring'):
            nx.draw_spring(G, with_labels=with_labels, node_color=color, node_size=node_size, arrows=with_arrows)
        elif (state_layout == 'planar'):
            nx.draw_planar(G, with_labels=with_labels, node_color=color, node_size=node_size, arrows=with_arrows)
        elif (state_layout == 'kamada-kawai'):
            nx.draw_kamada_kawai(G, with_labels=with_labels, node_color=color, node_size=node_size, arrows=with_arrows)
        elif isinstance(state_layout, dict):
            nx.draw(G, pos=state_layout, with_labels=with_labels, node_color=color, node_size=node_size, arrows=with_arrows)
        else:
            raise Exception(('unsupported layout: %s' % state_layout))
    ani = animation.FuncAnimation(fig, update, frames=list(enumerate(trajectory)), interval=interval, save_count=len(trajectory))
    if save:
        ani.save('evolved.gif', dpi=dpi, writer='imagemagick')
    if show:
        plt.show()
    return ani
