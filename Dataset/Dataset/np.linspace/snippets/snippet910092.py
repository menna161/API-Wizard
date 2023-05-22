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


def scatter2d(data_list, channels=[0, 1], xscale='logicle', yscale='logicle', xlabel=None, ylabel=None, xlim=None, ylim=None, title=None, color=None, savefig=None, **kwargs):
    "\n    Plot 2D scatter plot from one or more FCSData objects or numpy arrays.\n\n    Parameters\n    ----------\n    data_list : array or FCSData or list of array or list of FCSData\n        Flow cytometry data to plot.\n    channels : list of int, list of str\n        Two channels to use for the plot.\n    savefig : str, optional\n        The name of the file to save the figure to. If None, do not save.\n\n    Other parameters\n    ----------------\n    xscale : str, optional\n        Scale of the x axis, either ``linear``, ``log``, or ``logicle``.\n    yscale : str, optional\n        Scale of the y axis, either ``linear``, ``log``, or ``logicle``.\n    xlabel : str, optional\n        Label to use on the x axis. If None, attempts to extract channel\n        name from last data object.\n    ylabel : str, optional\n        Label to use on the y axis. If None, attempts to extract channel\n        name from last data object.\n    xlim : tuple, optional\n        Limits for the x axis. If None, attempts to extract limits from the\n        range of the last data object.\n    ylim : tuple, optional\n        Limits for the y axis. If None, attempts to extract limits from the\n        range of the last data object.\n    title : str, optional\n        Plot title.\n    color : matplotlib color or list of matplotlib colors, optional\n        Color for the scatter plot. It can be a list with the same length\n        as `data_list`. If `color` is not specified, elements from\n        `data_list` are plotted with colors taken from the module-level\n        variable `cmap_default`.\n    kwargs : dict, optional\n        Additional parameters passed directly to matploblib's ``scatter``.\n\n    Notes\n    -----\n    `scatter2d` calls matplotlib's ``scatter`` function for each object in\n    data_list. Additional keyword arguments provided to `scatter2d` are\n    passed directly to ``plt.scatter``.\n\n    "
    if (len(channels) != 2):
        raise ValueError('two channels need to be specified')
    if (not isinstance(data_list, list)):
        data_list = [data_list]
    if (color is None):
        color = [cmap_default(i) for i in np.linspace(0, 1, len(data_list))]
    if (not isinstance(color, list)):
        color = ([color] * len(data_list))
    for (i, data) in enumerate(data_list):
        data_plot = data[(:, channels)]
        plt.scatter(data_plot[(:, 0)], data_plot[(:, 1)], s=5, alpha=0.25, color=color[i], **kwargs)
    if (xlabel is not None):
        plt.xlabel(xlabel)
    elif hasattr(data_plot, 'channels'):
        plt.xlabel(data_plot.channels[0])
    if (ylabel is not None):
        plt.ylabel(ylabel)
    elif hasattr(data_plot, 'channels'):
        plt.ylabel(data_plot.channels[1])
    if (xscale == 'logicle'):
        plt.gca().set_xscale(xscale, data=data_list, channel=channels[0])
    else:
        plt.gca().set_xscale(xscale)
    if (yscale == 'logicle'):
        plt.gca().set_yscale(yscale, data=data_list, channel=channels[1])
    else:
        plt.gca().set_yscale(yscale)
    if (xlim is None):
        xlim = [np.inf, (- np.inf)]
        for data in data_list:
            if (hasattr(data, 'hist_bins') and hasattr(data.hist_bins, '__call__')):
                xlim_data = data.hist_bins(channels=channels[0], nbins=1, scale=xscale)
                xlim[0] = (xlim_data[0] if (xlim_data[0] < xlim[0]) else xlim[0])
                xlim[1] = (xlim_data[1] if (xlim_data[1] > xlim[1]) else xlim[1])
    plt.xlim(xlim)
    if (ylim is None):
        ylim = [np.inf, (- np.inf)]
        for data in data_list:
            if (hasattr(data, 'hist_bins') and hasattr(data.hist_bins, '__call__')):
                ylim_data = data.hist_bins(channels=channels[1], nbins=1, scale=yscale)
                ylim[0] = (ylim_data[0] if (ylim_data[0] < ylim[0]) else ylim[0])
                ylim[1] = (ylim_data[1] if (ylim_data[1] > ylim[1]) else ylim[1])
    plt.ylim(ylim)
    if (title is not None):
        plt.title(title)
    if (savefig is not None):
        plt.tight_layout()
        plt.savefig(savefig, dpi=savefig_dpi)
        plt.close()
