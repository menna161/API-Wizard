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


def hist1d(data_list, channel=0, xscale='logicle', bins=256, histtype='stepfilled', normed_area=False, normed_height=False, xlabel=None, ylabel=None, xlim=None, ylim=None, title=None, legend=False, legend_loc='best', legend_fontsize='medium', legend_labels=None, facecolor=None, edgecolor=None, savefig=None, **kwargs):
    "\n    Plot one 1D histogram from one or more flow cytometry data sets.\n\n    Parameters\n    ----------\n    data_list : FCSData or numpy array or list of FCSData or numpy array\n        Flow cytometry data to plot.\n    channel : int or str, optional\n        Channel from where to take the events to plot. If ndim == 1,\n        channel is ignored. String channel specifications are only\n        supported for data types which support string-based indexing\n        (e.g. FCSData).\n    xscale : str, optional\n        Scale of the x axis, either ``linear``, ``log``, or ``logicle``.\n    bins : int or array_like, optional\n        If `bins` is an integer, it specifies the number of bins to use.\n        If `bins` is an array, it specifies the bin edges to use. If `bins`\n        is None or an integer, `hist1d` will attempt to use\n        ``data.hist_bins`` to generate the bins automatically.\n    histtype : {'bar', 'barstacked', 'step', 'stepfilled'}, str, optional\n        Histogram type. Directly passed to ``plt.hist``.\n    normed_area : bool, optional\n        Flag indicating whether to normalize the histogram such that the\n        area under the curve is equal to one. The resulting plot is\n        equivalent to a probability density function.\n    normed_height : bool, optional\n        Flag indicating whether to normalize the histogram such that the\n        sum of all bins' heights is equal to one. The resulting plot is\n        equivalent to a probability mass function. `normed_height` is\n        ignored if `normed_area` is True.\n    savefig : str, optional\n        The name of the file to save the figure to. If None, do not save.\n\n    Other parameters\n    ----------------\n    xlabel : str, optional\n        Label to use on the x axis. If None, attempts to extract channel\n        name from last data object.\n    ylabel : str, optional\n        Label to use on the y axis. If None and ``normed_area==True``, use\n        'Probability'. If None, ``normed_area==False``, and\n        ``normed_height==True``, use 'Counts (normalized)'. If None,\n        ``normed_area==False``, and ``normed_height==False``, use 'Counts'.\n    xlim : tuple, optional\n        Limits for the x axis. If not specified and `bins` exists, use\n        the lowest and highest values of `bins`.\n    ylim : tuple, optional\n        Limits for the y axis.\n    title : str, optional\n        Plot title.\n    legend : bool, optional\n        Flag specifying whether to include a legend. If `legend` is True,\n        the legend labels will be taken from `legend_labels` if present,\n        else they will be taken from ``str(data_list[i])``.\n    legend_loc : str, optional\n        Location of the legend.\n    legend_fontsize : int or str, optional\n        Font size for the legend.\n    legend_labels : list, optional\n        Labels to use for the legend.\n    facecolor : matplotlib color or list of matplotlib colors, optional\n        The histogram's facecolor. It can be a list with the same length as\n        `data_list`. If `edgecolor` and `facecolor` are not specified, and\n        ``histtype == 'stepfilled'``, the facecolor will be taken from the\n        module-level variable `cmap_default`.\n    edgecolor : matplotlib color or list of matplotlib colors, optional\n        The histogram's edgecolor. It can be a list with the same length as\n        `data_list`. If `edgecolor` and `facecolor` are not specified, and\n        ``histtype == 'step'``, the edgecolor will be taken from the\n        module-level variable `cmap_default`.\n    kwargs : dict, optional\n        Additional parameters passed directly to matploblib's ``hist``.\n\n    Notes\n    -----\n    `hist1d` calls matplotlib's ``hist`` function for each object in\n    `data_list`. `hist_type`, the type of histogram to draw, is directly\n    passed to ``plt.hist``. Additional keyword arguments provided to\n    `hist1d` are passed directly to ``plt.hist``.\n\n    If `normed_area` is set to True, `hist1d` calls ``plt.hist`` with\n    ``density`` (or ``normed``, if matplotlib's version is older than\n    2.2.0) set to True. There is a bug in matplotlib 2.1.0 that\n    produces an incorrect plot in these conditions. We do not recommend\n    using matplotlib 2.1.0 if `normed_area` is expected to be used.\n\n    "
    if (normed_area and (packaging.version.parse(matplotlib.__version__) == packaging.version.parse('2.1.0'))):
        warnings.warn('bug in matplotlib 2.1.0 will result in an incorrect plot when normed_area is set to True')
    if (not isinstance(data_list, list)):
        data_list = [data_list]
    if (histtype == 'stepfilled'):
        if (facecolor is None):
            facecolor = [cmap_default(i) for i in np.linspace(0, 1, len(data_list))]
        if (edgecolor is None):
            edgecolor = (['black'] * len(data_list))
    elif (histtype == 'step'):
        if (edgecolor is None):
            edgecolor = [cmap_default(i) for i in np.linspace(0, 1, len(data_list))]
    if (not isinstance(edgecolor, list)):
        edgecolor = ([edgecolor] * len(data_list))
    if (not isinstance(facecolor, list)):
        facecolor = ([facecolor] * len(data_list))
    xscale_kwargs = {}
    if (xscale == 'logicle'):
        t = _LogicleTransform(data=data_list, channel=channel)
        xscale_kwargs['T'] = t.T
        xscale_kwargs['M'] = t.M
        xscale_kwargs['W'] = t.W
    for (i, data) in enumerate(data_list):
        hist_kwargs = kwargs.copy()
        if ('x' in hist_kwargs):
            raise ValueError('`x` must be specified via `data_list`')
        if (data.ndim > 1):
            hist_kwargs['x'] = data[(:, channel)]
        else:
            hist_kwargs['x'] = data
        hist_kwargs['bins'] = bins
        if (hasattr(hist_kwargs['x'], 'hist_bins') and hasattr(hist_kwargs['x'].hist_bins, '__call__')):
            if ((hist_kwargs['bins'] is None) or isinstance(hist_kwargs['bins'], int)):
                hist_kwargs['bins'] = hist_kwargs['x'].hist_bins(channels=0, nbins=hist_kwargs['bins'], scale=xscale, **xscale_kwargs)
        if ('density' in hist_kwargs):
            msg = 'use `normed_area` instead of `density`'
            raise ValueError(msg)
        if ('normed' in hist_kwargs):
            msg = 'use `normed_area` or `normed_height` instead of `normed`'
            raise ValueError(msg)
        if (packaging.version.parse(matplotlib.__version__) >= packaging.version.parse('2.2')):
            hist_kwargs['density'] = normed_area
        else:
            hist_kwargs['normed'] = normed_area
        if (normed_height and (not normed_area)):
            if ('weights' in hist_kwargs):
                msg = '`weights` must not be specified if'
                msg += ' `normed_height=True`'
                raise ValueError(msg)
            hist_kwargs['weights'] = np.ones_like(hist_kwargs['x'])
            hist_kwargs['weights'] /= float(len(hist_kwargs['x']))
        hist_kwargs['histtype'] = histtype
        hist_kwargs['facecolor'] = facecolor[i]
        hist_kwargs['edgecolor'] = edgecolor[i]
        (n, edges, patches) = plt.hist(**hist_kwargs)
    if (xscale == 'logicle'):
        plt.gca().set_xscale(xscale, data=data_list, channel=channel)
    else:
        plt.gca().set_xscale(xscale)
    if (xlabel is not None):
        plt.xlabel(xlabel)
    elif hasattr(hist_kwargs['x'], 'channels'):
        plt.xlabel(hist_kwargs['x'].channels[0])
    if (ylabel is not None):
        plt.ylabel(ylabel)
    elif normed_area:
        plt.ylabel('Probability')
    elif normed_height:
        plt.ylabel('Counts (normalized)')
    else:
        plt.ylabel('Counts')
    if (xlim is not None):
        plt.xlim(xlim)
    elif (bins is not None):
        plt.xlim((edges[0], edges[(- 1)]))
    if (ylim is not None):
        plt.ylim(ylim)
    if (title is not None):
        plt.title(title)
    if legend:
        if (legend_labels is None):
            legend_labels = [str(data) for data in data_list]
        plt.legend(legend_labels, loc=legend_loc, prop={'size': legend_fontsize})
    if (savefig is not None):
        plt.tight_layout()
        plt.savefig(savefig, dpi=savefig_dpi)
        plt.close()
