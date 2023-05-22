import glob
from matplotlib import pyplot as plt
import networkx as nx
import numpy as np
import pickle
import warnings
from matplotlib import cm
from .lplot import *


def getAxis(axis):
    if (axis is not False):
        ax = axis
        fig = ax.figure.canvas
    else:
        (fig, ax) = plt.subplots()
    return (fig, ax)
