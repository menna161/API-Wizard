import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import cv2
import shapely
from shapely.geometry import MultiLineString
from matplotlib.patches import PathPatch
from matplotlib import collections as mpl_collections
import matplotlib.path
import skimage.io


def plot_metric(C, diffs, routes_str=[], figsize=(10, 5), scatter_png='', hist_png='', scatter_alpha=0.3, scatter_size=2, scatter_cmap='jet', dpi=300):
    ' Plot output of cost metric in both scatterplot and histogram format'
    title = ('Path Length Similarity: ' + str(np.round(C, 2)))
    (fig, ax0) = plt.subplots(1, 1, figsize=((1 * figsize[0]), figsize[1]))
    ax0.scatter(list(range(len(diffs))), diffs, s=scatter_size, c=diffs, alpha=scatter_alpha, cmap=scatter_cmap)
    if (len(routes_str) > 0):
        xticklabel_pad = 0.1
        ax0.set_xticks(list(range(len(diffs))))
        ax0.set_xticklabels(routes_str, rotation=50, fontsize=4)
        ax0.tick_params(axis='x', which='major', pad=xticklabel_pad)
    ax0.set_ylabel('Length Diff (Normalized)')
    ax0.set_xlabel('Path ID')
    ax0.set_title(title)
    if scatter_png:
        plt.savefig(scatter_png, dpi=dpi)
    bins = np.linspace(0, 1, 30)
    bin_centers = np.mean(list(zip(bins, bins[1:])), axis=1)
    (hist, bin_edges) = np.histogram(diffs, bins=bins)
    (fig, ax1) = plt.subplots(nrows=1, ncols=1, figsize=figsize)
    ax1.bar(bin_centers, ((1.0 * hist) / len(diffs)), width=(bin_centers[1] - bin_centers[0]))
    ax1.set_xlim([0, 1])
    ax1.set_ylabel('Frac Num Routes')
    ax1.set_xlabel('Length Diff (Normalized)')
    ax1.set_title(('Length Diff Histogram - Score: ' + str(np.round(C, 2))))
    ax1.grid(True)
    if hist_png:
        plt.savefig(hist_png, dpi=dpi)
    return
