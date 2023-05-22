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


def plot_graph_on_im(G_, im_test_file, figsize=(8, 8), show_endnodes=False, width_key='speed_m/s', width_mult=0.125, color='lime', title='', figname='', default_node_size=15, max_speeds_per_line=12, dpi=300, plt_save_quality=75, ax=None, verbose=False):
    '\n    Overlay graph on image,\n    if width_key == int, use a constant width'
    try:
        im_cv2 = cv2.imread(im_test_file, 1)
        img_mpl = cv2.cvtColor(im_cv2, cv2.COLOR_BGR2RGB)
    except:
        img_sk = skimage.io.imread(im_test_file)
        if ((len(img_sk.shape) == 3) and (img_sk.shape[0] < 20)):
            img_mpl = np.moveaxis(img_sk, 0, (- 1))
        else:
            img_mpl = img_sk
    (h, w) = img_mpl.shape[:2]
    (node_x, node_y, lines, widths, title_vals) = ([], [], [], [], [])
    for (i, (u, v, edge_data)) in enumerate(G_.edges(data=True)):
        if (type(edge_data['geometry_pix']) == str):
            coords = list(shapely.wkt.loads(edge_data['geometry_pix']).coords)
        else:
            coords = list(edge_data['geometry_pix'].coords)
        if verbose:
            print('\n', i, u, v, edge_data)
            print('edge_data:', edge_data)
            print('  coords:', coords)
        lines.append(coords)
        node_x.append(coords[0][0])
        node_x.append(coords[(- 1)][0])
        node_y.append(coords[0][1])
        node_y.append(coords[(- 1)][1])
        if (type(width_key) == str):
            if verbose:
                print('edge_data[width_key]:', edge_data[width_key])
            width = int(np.rint((edge_data[width_key] * width_mult)))
            title_vals.append(int(np.rint(edge_data[width_key])))
        else:
            width = width_key
        widths.append(width)
    if (not ax):
        (fig, ax) = plt.subplots(1, 1, figsize=figsize)
    ax.imshow(img_mpl)
    if show_endnodes:
        ax.scatter(node_x, node_y, color=color, s=default_node_size, alpha=0.5)
    lc = mpl_collections.LineCollection(lines, colors=color, linewidths=widths, alpha=0.4, zorder=2)
    ax.add_collection(lc)
    ax.axis('off')
    if (len(title_vals) > 0):
        if verbose:
            print('title_vals:', title_vals)
        title_strs = np.sort(np.unique(title_vals)).astype(str)
        if (len(title_strs) > max_speeds_per_line):
            (n, b) = (max_speeds_per_line, title_strs)
            title_strs = np.insert(b, range(n, len(b), n), '\n')
        if verbose:
            print('title_strs:', title_strs)
        title = ((((title + '\n') + width_key) + ' = ') + ' '.join(title_strs))
    if title:
        ax.set_title(title)
    plt.tight_layout()
    print('title:', title)
    if title:
        plt.subplots_adjust(top=0.96)
    if verbose:
        print('img_mpl.shape:', img_mpl.shape)
    desired_dpi = int((np.max(img_mpl.shape) / np.max(figsize)))
    if verbose:
        print('desired dpi:', desired_dpi)
    dpi = int(np.min([3500, desired_dpi]))
    if verbose:
        print('plot dpi:', dpi)
    if figname:
        plt.savefig(figname, dpi=dpi, quality=plt_save_quality)
    return ax
