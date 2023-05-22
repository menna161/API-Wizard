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


def scatter3d(data_list, channels=[0, 1, 2], xscale='logicle', yscale='logicle', zscale='logicle', xlabel=None, ylabel=None, zlabel=None, xlim=None, ylim=None, zlim=None, title=None, color=None, savefig=None, **kwargs):
    "\n    Plot 3D scatter plot from one or more FCSData objects or numpy arrays.\n\n    Parameters\n    ----------\n    data_list : array or FCSData or list of array or list of FCSData\n        Flow cytometry data to plot.\n    channels : list of int, list of str\n        Three channels to use for the plot.\n    savefig : str, optional\n        The name of the file to save the figure to. If None, do not save.\n\n    Other parameters\n    ----------------\n    xscale : str, optional\n        Scale of the x axis, either ``linear``, ``log``, or ``logicle``.\n    yscale : str, optional\n        Scale of the y axis, either ``linear``, ``log``, or ``logicle``.\n    zscale : str, optional\n        Scale of the z axis, either ``linear``, ``log``, or ``logicle``.\n    xlabel : str, optional\n        Label to use on the x axis. If None, attempts to extract channel\n        name from last data object.\n    ylabel : str, optional\n        Label to use on the y axis. If None, attempts to extract channel\n        name from last data object.\n    zlabel : str, optional\n        Label to use on the z axis. If None, attempts to extract channel\n        name from last data object.\n    xlim : tuple, optional\n        Limits for the x axis. If None, attempts to extract limits from the\n        range of the last data object.\n    ylim : tuple, optional\n        Limits for the y axis. If None, attempts to extract limits from the\n        range of the last data object.\n    zlim : tuple, optional\n        Limits for the z axis. If None, attempts to extract limits from the\n        range of the last data object.\n    title : str, optional\n        Plot title.\n    color : matplotlib color or list of matplotlib colors, optional\n        Color for the scatter plot. It can be a list with the same length\n        as `data_list`. If `color` is not specified, elements from\n        `data_list` are plotted with colors taken from the module-level\n        variable `cmap_default`.\n    kwargs : dict, optional\n        Additional parameters passed directly to matploblib's ``scatter``.\n\n    Notes\n    -----\n    `scatter3d` uses matplotlib's ``scatter`` with a 3D projection.\n    Additional keyword arguments provided to `scatter3d` are passed\n    directly to ``scatter``.\n\n    "
    if (len(channels) != 3):
        raise ValueError('three channels need to be specified')
    if (not isinstance(data_list, list)):
        data_list = [data_list]
    if (color is None):
        color = [cmap_default(i) for i in np.linspace(0, 1, len(data_list))]
    if (not isinstance(color, list)):
        color = ([color] * len(data_list))
    if (xscale == 'linear'):
        xscale_transform = (lambda x: x)
    elif (xscale == 'log'):
        xscale_transform = np.log10
    elif (xscale == 'logicle'):
        t = _LogicleTransform(data=data_list, channel=channels[0])
        it = _InterpolatedInverseTransform(t, 0, t.M)
        xscale_transform = it.transform_non_affine
    else:
        raise ValueError('scale {} not supported'.format(xscale))
    if (yscale == 'linear'):
        yscale_transform = (lambda x: x)
    elif (yscale == 'log'):
        yscale_transform = np.log10
    elif (yscale == 'logicle'):
        t = _LogicleTransform(data=data_list, channel=channels[1])
        it = _InterpolatedInverseTransform(t, 0, t.M)
        yscale_transform = it.transform_non_affine
    else:
        raise ValueError('scale {} not supported'.format(yscale))
    if (zscale == 'linear'):
        zscale_transform = (lambda x: x)
    elif (zscale == 'log'):
        zscale_transform = np.log10
    elif (zscale == 'logicle'):
        t = _LogicleTransform(data=data_list, channel=channels[2])
        it = _InterpolatedInverseTransform(t, 0, t.M)
        zscale_transform = it.transform_non_affine
    else:
        raise ValueError('scale {} not supported'.format(zscale))
    ax_3d = plt.gca(projection='3d')
    for (i, data) in enumerate(data_list):
        data_plot = data[(:, channels)]
        ax_3d.scatter(xscale_transform(data_plot[(:, 0)]), yscale_transform(data_plot[(:, 1)]), zscale_transform(data_plot[(:, 2)]), marker='o', alpha=0.1, color=color[i], **kwargs)
    ax_3d.xaxis.set_ticklabels([])
    ax_3d.yaxis.set_ticklabels([])
    ax_3d.zaxis.set_ticklabels([])
    if (xlabel is not None):
        ax_3d.set_xlabel(xlabel)
    elif hasattr(data_plot, 'channels'):
        ax_3d.set_xlabel(data_plot.channels[0])
    if (ylabel is not None):
        ax_3d.set_ylabel(ylabel)
    elif hasattr(data_plot, 'channels'):
        ax_3d.set_ylabel(data_plot.channels[1])
    if (zlabel is not None):
        ax_3d.set_zlabel(zlabel)
    elif hasattr(data_plot, 'channels'):
        ax_3d.set_zlabel(data_plot.channels[2])
    if (xlim is None):
        xlim = np.array([np.inf, (- np.inf)])
        for data in data_list:
            if (hasattr(data, 'hist_bins') and hasattr(data.hist_bins, '__call__')):
                xlim_data = data.hist_bins(channels=channels[0], nbins=1, scale=xscale)
                xlim[0] = (xlim_data[0] if (xlim_data[0] < xlim[0]) else xlim[0])
                xlim[1] = (xlim_data[1] if (xlim_data[1] > xlim[1]) else xlim[1])
        xlim = xscale_transform(xlim)
    ax_3d.set_xlim(xlim)
    if (ylim is None):
        ylim = np.array([np.inf, (- np.inf)])
        for data in data_list:
            if (hasattr(data, 'hist_bins') and hasattr(data.hist_bins, '__call__')):
                ylim_data = data.hist_bins(channels=channels[1], nbins=1, scale=yscale)
                ylim[0] = (ylim_data[0] if (ylim_data[0] < ylim[0]) else ylim[0])
                ylim[1] = (ylim_data[1] if (ylim_data[1] > ylim[1]) else ylim[1])
        ylim = yscale_transform(ylim)
    ax_3d.set_ylim(ylim)
    if (zlim is None):
        zlim = np.array([np.inf, (- np.inf)])
        for data in data_list:
            if (hasattr(data, 'hist_bins') and hasattr(data.hist_bins, '__call__')):
                zlim_data = data.hist_bins(channels=channels[2], nbins=1, scale=zscale)
                zlim[0] = (zlim_data[0] if (zlim_data[0] < zlim[0]) else zlim[0])
                zlim[1] = (zlim_data[1] if (zlim_data[1] > zlim[1]) else zlim[1])
        zlim = zscale_transform(zlim)
    ax_3d.set_zlim(zlim)
    if (title is not None):
        plt.title(title)
    if (savefig is not None):
        plt.tight_layout()
        plt.savefig(savefig, dpi=savefig_dpi)
        plt.close()
