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


def density_and_hist(data, gated_data=None, gate_contour=None, density_channels=None, density_params={}, hist_channels=None, hist_params={}, figsize=None, savefig=None):
    "\n    Make a combined density/histogram plot of a FCSData object.\n\n    This function calls `hist1d` and `density2d` to plot a density diagram\n    and a number of histograms in different subplots of the same plot using\n    one single function call. Setting `density_channels` to None will not\n    produce a density diagram, and setting `hist_channels` to None will not\n    produce any histograms. Setting both to None will raise an error.\n    Additional parameters can be provided to `density2d` and `hist1d` by\n    using `density_params` and `hist_params`.\n\n    If `gated_data` is provided, this function will plot the histograms\n    corresponding to `gated_data` on top of `data`'s histograms, with some\n    transparency on `data`. In addition, a legend will be added with the\n    labels 'Ungated' and 'Gated'. If `gate_contour` is provided and it\n    contains a valid list of 2D curves, these will be plotted on top of the\n    density plot.\n\n    Parameters\n    ----------\n    data : FCSData object\n        Flow cytometry data object to plot.\n    gated_data : FCSData object, optional\n        Flow cytometry data object. If `gated_data` is specified, the\n        histograms of `data` are plotted with an alpha value of 0.5, and\n        the histograms of `gated_data` are plotted on top of those with\n        an alpha value of 1.0.\n    gate_contour : list, optional\n        List of Nx2 curves, representing a gate contour to be plotted in\n        the density diagram.\n    density_channels : list\n        Two channels to use for the density plot. If `density_channels` is\n        None, do not plot a density plot.\n    density_params : dict, optional\n        Parameters to pass to `density2d`.\n    hist_channels : list\n        Channels to use for each histogram. If `hist_channels` is None,\n        do not plot histograms.\n    hist_params : list, optional\n        List of dictionaries with the parameters to pass to each call of\n        `hist1d`.\n    savefig : str, optional\n        The name of the file to save the figure to. If None, do not save.\n\n    Other parameters\n    ----------------\n    figsize : tuple, optional\n        Figure size. If None, calculate a default based on the number of\n        subplots.\n\n    Raises\n    ------\n    ValueError\n        If both `density_channels` and `hist_channels` are None.\n\n    "
    if ((density_channels is None) and (hist_channels is None)):
        raise ValueError('density_channels and hist_channels cannot be both None')
    if (not hasattr(hist_channels, '__iter__')):
        hist_channels = [hist_channels]
    if isinstance(hist_params, dict):
        hist_params = ([hist_params] * len(hist_channels))
    plot_density = (not (density_channels is None))
    n_plots = (plot_density + len(hist_channels))
    if (figsize is None):
        height = (0.315 + (2.935 * n_plots))
        figsize = (6, height)
    plt.figure(figsize=figsize)
    if plot_density:
        plt.subplot(n_plots, 1, 1)
        density2d(data, channels=density_channels, **density_params)
        if (gate_contour is not None):
            for g in gate_contour:
                plt.plot(g[(:, 0)], g[(:, 1)], color='k', linewidth=1.25)
        if ('title' not in density_params):
            if (gated_data is not None):
                ret = ((gated_data.shape[0] * 100.0) / data.shape[0])
                title = '{} ({:.1f}% retained)'.format(str(data), ret)
            else:
                title = str(data)
            plt.title(title)
    n_colors = (n_plots - 1)
    default_property_cycler = plt.rcParams['axes.prop_cycle']()
    colors = [next(default_property_cycler)['color'] for i in range(n_colors)]
    for (i, hist_channel) in enumerate(hist_channels):
        plt.subplot(n_plots, 1, ((plot_density + i) + 1))
        hist_params_i = hist_params[i].copy()
        if ('facecolor' not in hist_params_i):
            hist_params_i['facecolor'] = colors[i]
        if (gated_data is not None):
            hist1d(data, channel=hist_channel, alpha=0.5, **hist_params_i)
            hist1d(gated_data, channel=hist_channel, alpha=1.0, **hist_params_i)
            plt.legend(['Ungated', 'Gated'], loc='best', fontsize='medium')
        else:
            hist1d(data, channel=hist_channel, **hist_params_i)
    if (savefig is not None):
        plt.tight_layout()
        plt.savefig(savefig, dpi=savefig_dpi)
        plt.close()
