from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
import sys
from domain.config import games


def getNodeCoord(G, layer, taskName):
    env = games[taskName]
    nIn = (env.input_size + 1)
    nOut = env.output_size
    nNode = len(G.nodes)
    fixed_pos = np.empty((nNode, 2))
    fixed_nodes = np.r_[(np.arange(0, nIn), np.arange((nNode - nOut), nNode))]
    fig_wide = 10
    fig_long = 5
    x = (np.ones((1, nNode)) * layer)
    x = ((x / np.max(x)) * fig_wide)
    (_, nPerLayer) = np.unique(layer, return_counts=True)
    y = cLinspace((- 2), (fig_long + 2), nPerLayer[0])
    for i in range(1, len(nPerLayer)):
        if ((i % 2) == 0):
            y = np.r_[(y, cLinspace(0, fig_long, nPerLayer[i]))]
        else:
            y = np.r_[(y, cLinspace((- 1), (fig_long + 1), nPerLayer[i]))]
    fixed_pos = np.c_[(x.T, y.T)]
    pos = dict(enumerate(fixed_pos.tolist()))
    return pos
