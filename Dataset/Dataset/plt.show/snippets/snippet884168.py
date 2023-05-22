import numpy as np
import torch
import torch.nn.functional as F
import matplotlib
import threading
from matplotlib import collections as mc
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation
import time
import copy
import math
from neural_layout.barnes_hut_tree import *
from matplotlib import pyplot as plt


def plot_on(self, plot, plot_connections=True):
    try:
        plot.lines.remove()
        plot.scatter.remove()
    except:
        pass
    if plot_connections:
        plot.lines = mc.LineCollection(self.line_data(), lw=0.5, alpha=0.2)
        plot.ax.add_collection(plot.lines)
    plot.scatter = plot.ax.scatter(self.positions[(:, 0)], self.positions[(:, 1)], linewidths=1, c=self.colors)
    plot.ax.autoscale()
    plot.fig.canvas.draw()
    plt.show()
