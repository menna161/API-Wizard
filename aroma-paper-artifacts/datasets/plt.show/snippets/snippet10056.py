import math
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def plot_tour(self, G, pos):
    '\n        Renders the points and tour.\n        :param G: a NetworkX Graph representing the points and the tour\n        :param pos: a dictionary defining the NetworkX positions for the Graph\n        '
    nx.draw_networkx(G, pos)
    plt.show()
