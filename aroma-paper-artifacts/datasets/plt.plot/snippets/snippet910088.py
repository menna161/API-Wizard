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


def _plot_single_violin(violin_position, violin_data, violin_width, violin_kwargs, bin_edges, density, vert, scale, upper_trim_fraction, lower_trim_fraction, draw_summary_stat, draw_summary_stat_fxn, draw_summary_stat_kwargs):
    '\n    Plot a single violin.\n\n    Illustrate the relative frequency of members of a population using a\n    normalized, symmetrical histogram ("violin") centered at a corresponding\n    position. Wider regions of the violin indicate regions that occur with\n    greater frequency.\n\n    Parameters\n    ----------\n    violin_position : scalar\n        Position at which to center violin.\n    violin_data : 1D array\n        A population for which to plot a violin.\n    violin_width : scalar\n        Width of violin. If `scale` is ``log``, the units are decades.\n    violin_kwargs : dict\n        Keyword arguments passed to the ``plt.fill_between()`` command that\n        illustrates the violin.\n    bin_edges : array\n        Bin edges used to bin population members.\n    density : bool\n        `density` parameter passed to the ``np.histogram()`` command that bins\n        population members. If True, violin width represents relative\n        frequency *density* instead of relative frequency (i.e., bins are\n        normalized by their width).\n    vert : bool\n        Flag specifying to illustrate a vertical violin. If False, a\n        horizontal violin is illustrated.\n    scale : {\'linear\', \'log\'}\n        Scale of the position axis (x-axis if `vert` is True, y-axis if `vert`\n        is False).\n    upper_trim_fraction : float\n        Fraction of members to trim (discard) from the top of the violin\n        (e.g., for aesthetic purposes).\n    lower_trim_fraction : float\n        Fraction of members to trim (discard) from the bottom of the violin\n        (e.g., for aesthetic purposes).\n    draw_summary_stat : bool\n        Flag specifying to illustrate a summary statistic.\n    draw_summary_stat_fxn : function\n        Function used to calculate the summary statistic. The summary\n        statistic is calculated prior to aesthetic trimming.\n    draw_summary_stat_kwargs : dict\n        Keyword arguments passed to the ``plt.plot()`` command that\n        illustrates the summary statistic.\n\n    '
    summary_stat = None
    violin_regions = []
    if (len(violin_data) > 0):
        if draw_summary_stat:
            summary_stat = draw_summary_stat_fxn(violin_data)
        num_discard_low = int(np.floor((len(violin_data) * float(lower_trim_fraction))))
        num_discard_high = int(np.floor((len(violin_data) * float(upper_trim_fraction))))
        violin_data = np.sort(violin_data)
        violin_data = violin_data[num_discard_low:]
        violin_data = violin_data[::(- 1)]
        violin_data = violin_data[num_discard_high:]
        violin_data = violin_data[::(- 1)]
        (H, H_edges) = np.histogram(violin_data, bins=bin_edges, density=density)
        H = np.array(H, dtype=float)
        positive_edge = np.repeat(H, 2)
        positive_edge = np.insert(positive_edge, 0, 0.0)
        positive_edge = np.append(positive_edge, 0.0)
        positive_edge /= np.max(positive_edge)
        positive_edge *= (violin_width / 2.0)
        if (scale == 'log'):
            negative_edge = (np.log10(violin_position) - positive_edge)
            positive_edge = (np.log10(violin_position) + positive_edge)
            positive_edge = (10 ** positive_edge)
            negative_edge = (10 ** negative_edge)
        else:
            negative_edge = (violin_position - positive_edge)
            positive_edge = (violin_position + positive_edge)
        height = np.repeat(H_edges, 2)
        idx = 0
        if (len(height) == 1):
            if (positive_edge[idx] == negative_edge[idx]):
                pass
            else:
                violin_regions.append(_ViolinRegion(positive_edge=positive_edge, negative_edge=negative_edge, height=height))
        else:
            start = idx
            while (idx < (len(height) - 1)):
                if ((positive_edge[idx] == negative_edge[idx]) and (positive_edge[(idx + 1)] != negative_edge[(idx + 1)])):
                    start = idx
                elif ((positive_edge[idx] != negative_edge[idx]) and (positive_edge[(idx + 1)] != negative_edge[(idx + 1)])):
                    pass
                elif ((positive_edge[idx] != negative_edge[idx]) and (positive_edge[(idx + 1)] == negative_edge[(idx + 1)])):
                    end = (idx + 1)
                    violin_regions.append(_ViolinRegion(positive_edge=positive_edge[start:(end + 1)], negative_edge=negative_edge[start:(end + 1)], height=height[start:(end + 1)]))
                    start = None
                elif ((positive_edge[idx] == negative_edge[idx]) and (positive_edge[(idx + 1)] == negative_edge[(idx + 1)])):
                    start = None
                idx += 1
            if (start is not None):
                end = idx
                violin_regions.append(_ViolinRegion(positive_edge=positive_edge[start:(end + 1)], negative_edge=negative_edge[start:(end + 1)], height=height[start:(end + 1)]))
    if vert:
        for vr in violin_regions:
            plt.fill_betweenx(x1=vr.negative_edge, x2=vr.positive_edge, y=vr.height, **violin_kwargs)
    else:
        for vr in violin_regions:
            plt.fill_between(y1=vr.positive_edge, y2=vr.negative_edge, x=vr.height, **violin_kwargs)
    if (draw_summary_stat and (summary_stat is not None)):
        if (scale == 'log'):
            positive_edge = (np.log10(violin_position) + (violin_width / 2.0))
            negative_edge = (np.log10(violin_position) - (violin_width / 2.0))
            positive_edge = (10 ** positive_edge)
            negative_edge = (10 ** negative_edge)
        else:
            positive_edge = (violin_position + (violin_width / 2.0))
            negative_edge = (violin_position - (violin_width / 2.0))
        if vert:
            plt.plot([negative_edge, positive_edge], [summary_stat, summary_stat], **draw_summary_stat_kwargs)
        else:
            plt.plot([summary_stat, summary_stat], [negative_edge, positive_edge], **draw_summary_stat_kwargs)
