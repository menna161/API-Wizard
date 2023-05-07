import netomaton as ntm
import numpy as np


def perturb(pctx):
    '\n        Mutates the value of the node with index 100 at each timestep, making it either 0 or 1 randomly.\n        '
    if (pctx.node_label == 100):
        return np.random.randint(2)
    return pctx.node_activity
