import time
import math
import numpy as np
import pandas as pd
import geopandas as gpd
import networkx as nx
from shapely.geometry import Point
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import LineString


def save_and_show(fig, ax, save, show, close, file_format, dpi, axis_off, filename=''):
    "\n    Save a figure to disk and show it, as specified.\n    Parameters\n    ----------\n    fig : figure\n    ax : axis\n    save : bool\n        whether to save the figure to disk or not\n    show : bool\n        whether to display the figure or not\n    close : bool\n        close the figure (only if show equals False) to prevent display\n    filename : string\n        the name of the file to save\n    file_format : string\n        the format of the file to save (e.g., 'jpg', 'png', 'svg')\n    dpi : int\n        the resolution of the image file if saving\n    axis_off : bool\n        if True matplotlib axis was turned off by plot_graph so constrain the\n        saved figure's extent to the interior of the axis\n    Returns\n    -------\n    fig, ax : tuple\n    "
    if save:
        start_time = time.time()
        path_filename = filename
        if (file_format == 'svg'):
            ax.axis('off')
            ax.set_position([0, 0, 1, 1])
            ax.patch.set_alpha(0.0)
            fig.patch.set_alpha(0.0)
            if (len(filename) > 0):
                fig.savefig(path_filename, bbox_inches=0, format=file_format, facecolor=fig.get_facecolor(), transparent=True)
        else:
            if axis_off:
                extent = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
            else:
                extent = 'tight'
            if (len(filename) > 0):
                fig.savefig(path_filename, dpi=dpi, bbox_inches=extent, format=file_format, facecolor=fig.get_facecolor(), transparent=True)
    if show:
        start_time = time.time()
        plt.show()
    elif close:
        plt.close()
    return (fig, ax)
