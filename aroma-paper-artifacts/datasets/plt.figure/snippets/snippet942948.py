import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.font_manager import FontProperties
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tadataka.plot.common import axis3d


def plot2d(P: np.ndarray, do_annotate=False, color=None):
    '\n    Plot 2D points\n\n    Args:\n        P: 2D array of shape (n_points, 2)\n        do_annotate: Annotate points if True\n        color: Color of points\n    '
    if (color is None):
        color = object_color(P)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(P[(:, 0)], P[(:, 1)], c=color)
    if do_annotate:
        annotate(ax, P)
    ax.set_xlabel('x axis')
    ax.set_ylabel('y axis')
    ax.set_aspect('equal', 'datalim')
    return ax
