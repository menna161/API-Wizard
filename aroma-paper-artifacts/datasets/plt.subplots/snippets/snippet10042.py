from math import *
import matplotlib as mpl
import matplotlib.animation as animation
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import numpy as np
from .utils import get_activities_over_time_as_list
from matplotlib.patches import RegularPolygon
from matplotlib.collections import PatchCollection


def plot_hex_grid(trajectory, shape=None, slice=(- 1), title='', colormap='Greys', vmin=None, vmax=None, edgecolor=None):
    activities = get_activities_over_time_as_list(trajectory)
    if (shape is not None):
        activities = np.array(activities).reshape((len(activities), shape[0], shape[1]))[slice]
    triples = _get_triples(activities)
    has_odd_rows = ((len(activities) % 2) != 0)
    (fig, ax) = plt.subplots(1)
    ax.set_aspect('equal')
    m = _get_scaled_colormap(triples, colormap, vmin, vmax)
    for t in triples:
        (x, y) = (_oddr_offset_to_pixel(t[0], t[1]) if has_odd_rows else _evenr_offset_to_pixel(t[0], t[1]))
        hex = RegularPolygon((x, y), numVertices=6, radius=1.0, orientation=np.radians(60), facecolor=m.to_rgba(t[2]), edgecolor=edgecolor)
        ax.add_patch(hex)
    ax.scatter([t[0] for t in triples], [t[1] for t in triples], marker='')
    plt.gca().invert_yaxis()
    plt.title(title)
    plt.show()
