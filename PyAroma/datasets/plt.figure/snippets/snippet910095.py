import packaging
import packaging.version
import collections
import numpy as np
import scipy.ndimage.filters
import matplotlib
import matplotlib.scale
import matplotlib.transforms
import matplotlib.ticker
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.font_manager import FontProperties
import warnings


def scatter3d_and_projections(data_list, channels=[0, 1, 2], xscale='logicle', yscale='logicle', zscale='logicle', xlabel=None, ylabel=None, zlabel=None, xlim=None, ylim=None, zlim=None, color=None, figsize=None, savefig=None, **kwargs):
    "\n    Plot a 3D scatter plot and 2D projections from FCSData objects.\n\n    `scatter3d_and_projections` creates a 3D scatter plot and three 2D\n    projected scatter plots in four different axes for each FCSData object\n    in `data_list`, in the same figure.\n\n    Parameters\n    ----------\n    data_list : FCSData object, or list of FCSData objects\n        Flow cytometry data to plot.\n    channels : list of int, list of str\n        Three channels to use for the plot.\n    savefig : str, optional\n        The name of the file to save the figure to. If None, do not save.\n\n    Other parameters\n    ----------------\n    xscale : str, optional\n        Scale of the x axis, either ``linear``, ``log``, or ``logicle``.\n    yscale : str, optional\n        Scale of the y axis, either ``linear``, ``log``, or ``logicle``.\n    zscale : str, optional\n        Scale of the z axis, either ``linear``, ``log``, or ``logicle``.\n    xlabel : str, optional\n        Label to use on the x axis. If None, attempts to extract channel\n        name from last data object.\n    ylabel : str, optional\n        Label to use on the y axis. If None, attempts to extract channel\n        name from last data object.\n    zlabel : str, optional\n        Label to use on the z axis. If None, attempts to extract channel\n        name from last data object.\n    xlim : tuple, optional\n        Limits for the x axis. If None, attempts to extract limits from the\n        range of the last data object.\n    ylim : tuple, optional\n        Limits for the y axis. If None, attempts to extract limits from the\n        range of the last data object.\n    zlim : tuple, optional\n        Limits for the z axis. If None, attempts to extract limits from the\n        range of the last data object.\n    color : matplotlib color or list of matplotlib colors, optional\n        Color for the scatter plot. It can be a list with the same length\n        as `data_list`. If `color` is not specified, elements from\n        `data_list` are plotted with colors taken from the module-level\n        variable `cmap_default`.\n    figsize : tuple, optional\n        Figure size. If None, use matplotlib's default.\n    kwargs : dict, optional\n        Additional parameters passed directly to matploblib's ``scatter``.\n\n    Notes\n    -----\n    `scatter3d_and_projections` uses matplotlib's ``scatter``, with the 3D\n    scatter plot using a 3D projection. Additional keyword arguments\n    provided to `scatter3d_and_projections` are passed directly to\n    ``scatter``.\n\n    "
    if (len(channels) != 3):
        raise ValueError('three channels need to be specified')
    plt.figure(figsize=figsize)
    plt.subplot(221)
    scatter2d(data_list, channels=[channels[0], channels[2]], xscale=xscale, yscale=zscale, xlabel=xlabel, ylabel=zlabel, xlim=xlim, ylim=zlim, color=color, **kwargs)
    ax_3d = plt.gcf().add_subplot(222, projection='3d')
    scatter3d(data_list, channels=channels, xscale=xscale, yscale=yscale, zscale=zscale, xlabel=xlabel, ylabel=ylabel, zlabel=zlabel, xlim=xlim, ylim=ylim, zlim=zlim, color=color, **kwargs)
    plt.subplot(223)
    scatter2d(data_list, channels=[channels[0], channels[1]], xscale=xscale, yscale=yscale, xlabel=xlabel, ylabel=ylabel, xlim=xlim, ylim=ylim, color=color, **kwargs)
    plt.subplot(224)
    scatter2d(data_list, channels=[channels[2], channels[1]], xscale=zscale, yscale=yscale, xlabel=zlabel, ylabel=ylabel, xlim=zlim, ylim=ylim, color=color, **kwargs)
    if (savefig is not None):
        plt.tight_layout()
        plt.savefig(savefig, dpi=savefig_dpi)
        plt.close()
