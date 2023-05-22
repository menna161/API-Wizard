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


def _plot_gt_prop_graphs(G_gt, G_prop, im_test_file, figsize=(16, 8), show_endnodes=False, width_key='Inferred Speed (mph)', width_mult=0.125, gt_color='cyan', prop_color='lime', default_node_size=15, title='', figname='', adjust=True, verbose=False):
    'Plot the ground truth, and prediction mask Overlay graph on image,\n    if width_key == int, use a constant width'
    (fig, (ax0, ax1)) = plt.subplots(1, 2, figsize=figsize)
    print('Plotting ground truth...')
    _ = plot_graph_on_im(G_gt, im_test_file, figsize=figsize, show_endnodes=show_endnodes, width_key=width_key, width_mult=width_mult, color=gt_color, default_node_size=default_node_size, title=('Ground Truth:  ' + title), figname='', ax=ax0, verbose=verbose)
    print('Plotting proposal...')
    _ = plot_graph_on_im(G_prop, im_test_file, figsize=figsize, show_endnodes=show_endnodes, width_key=width_key, width_mult=width_mult, color=prop_color, default_node_size=default_node_size, title=('Proposal:  ' + title), figname='', ax=ax1, verbose=verbose)
    plt.tight_layout()
    if adjust:
        plt.subplots_adjust(top=0.96)
    if figname:
        plt.savefig(figname, dpi=300)
    return fig
