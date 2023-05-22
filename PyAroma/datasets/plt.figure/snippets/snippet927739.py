from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
import sys
from domain.config import games


def viewInd(ind, taskName):
    env = games[taskName]
    if isinstance(ind, str):
        ind = np.loadtxt(ind, delimiter=',')
        wMat = ind[(:, :(- 1))]
        aVec = ind[(:, (- 1))]
    else:
        wMat = ind.wMat
        aVec = np.zeros(np.shape(wMat)[0])
    print('# of Connections in ANN: ', np.sum((wMat != 0)))
    nIn = (env.input_size + 1)
    nOut = env.output_size
    (G, layer) = ind2graph(wMat, nIn, nOut)
    pos = getNodeCoord(G, layer, taskName)
    fig = plt.figure(figsize=(10, 10), dpi=100)
    ax = fig.add_subplot(111)
    drawEdge(G, pos, wMat, layer)
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_shape='o', cmap='terrain', vmin=0, vmax=6)
    drawNodeLabels(G, pos, aVec)
    labelInOut(pos, env)
    plt.tick_params(axis='both', which='both', bottom=False, top=False, left=False, labelleft=False, labelbottom=False)
    return (fig, ax)
