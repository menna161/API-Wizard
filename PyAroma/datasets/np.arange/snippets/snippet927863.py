from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
import sys
from domain.config import games


def labelInOut(pos, env):
    nIn = (env.input_size + 1)
    nOut = env.output_size
    nNode = len(pos)
    fixed_nodes = np.r_[(np.arange(0, nIn), np.arange((nNode - nOut), nNode))]
    if (len(env.in_out_labels) > 0):
        stateLabels = (['bias'] + env.in_out_labels)
        labelDict = {}
    for i in range(len(stateLabels)):
        labelDict[fixed_nodes[i]] = stateLabels[i]
    for i in range(nIn):
        plt.annotate(labelDict[i], xy=((pos[i][0] - 0.5), pos[i][1]), xytext=((pos[i][0] - 2.5), (pos[i][1] - 0.5)), arrowprops=dict(arrowstyle='->', color='k', connectionstyle='angle'))
    for i in range((nNode - nOut), nNode):
        plt.annotate(labelDict[i], xy=((pos[i][0] + 0.1), pos[i][1]), xytext=((pos[i][0] + 1.5), (pos[i][1] + 1.0)), arrowprops=dict(arrowstyle='<-', color='k', connectionstyle='angle'))
