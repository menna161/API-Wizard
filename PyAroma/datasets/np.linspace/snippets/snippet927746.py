from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
import sys
from domain.config import games


def cLinspace(start, end, N):
    if (N == 1):
        return np.mean([start, end])
    else:
        return np.linspace(start, end, N)
