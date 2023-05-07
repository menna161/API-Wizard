import tensorflow as tf
from circle_loss import SparseAmsoftmaxLoss, SparseCircleLoss
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import cycler
import numpy as np
from typing import List


def build_ball(ax):
    xlm = ax.get_xlim3d()
    ylm = ax.get_ylim3d()
    zlm = ax.get_zlim3d()
    ax.set_xlim3d((- 0.82), 0.82)
    ax.set_ylim3d((- 0.82), 0.82)
    ax.set_zlim3d((- 0.82), 0.82)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('w')
    ax.yaxis.pane.set_edgecolor('w')
    ax.zaxis.pane.set_edgecolor('w')
    ax.grid(False)
    ax.set_xticks([(- 0.5), 0, 0.5])
    ax.set_yticks([(- 0.5), 0, 0.5])
    ax.set_zticks([(- 1), (- 0.5), 0, 0.5, 1])
    u = np.linspace(0, (2 * np.pi), 15)
    v = np.linspace(0, np.pi, 20)
    x = (1 * np.outer(np.cos(u), np.sin(v)))
    y = (1 * np.outer(np.sin(u), np.sin(v)))
    z = (1 * np.outer(np.ones(np.size(u)), np.cos(v)))
    ax.plot_wireframe(x, y, z, colors='dimgray', alpha=0.6, linestyles='-', linewidths=1)
