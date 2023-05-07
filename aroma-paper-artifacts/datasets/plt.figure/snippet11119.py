import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def plot_3d_func(X, Y, Z, zlabel, figsize):
    'Plot a 3 dimensional function.\n\n    Plots a 3 dimensional function, where X, Y, Z form a meshgrid, with the\n    usual functional relationship: z = f(x, y).\n\n    Args:\n        X (np.array): Meshgrid on first dimension.\n        Y (np.array): Meshgrid on second dimension.\n        Z (np.array): Meshgrid on outcome dimensions.\n        zlabel (str): Name of z-axis.\n        figsize (tuple): Figure size.\n\n    Returns:\n        ax (matplotlib.axis): The finished plot.\n\n    '
    mpl.rcParams.update({'font.family': 'stix'})
    mpl.rcParams.update({'font.size': 30})
    plt.rcParams.update({'font.size': 22})
    fig = plt.figure()
    ax = fig.gca(projection=Axes3D.name)
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='viridis', edgecolor='none')
    ax.set_xlabel('x1')
    ax.set_ylabel('x2')
    ax.set_zlabel(zlabel)
    ax.set_zlim((0, 5))
    ax.yaxis.labelpad = 30
    ax.zaxis.labelpad = 10
    ax.xaxis.labelpad = 30
    ax.view_init(30, 240)
    ax.grid(False)
    ax.xaxis.pane.set_edgecolor('black')
    ax.yaxis.pane.set_edgecolor('black')
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    plt.rcParams['figure.figsize'] = [figsize[0], figsize[1]]
