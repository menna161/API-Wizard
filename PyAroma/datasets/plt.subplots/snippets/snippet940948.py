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


def plot_graph(G, bbox=None, fig_height=6, fig_width=None, margin=0.02, axis_off=True, equal_aspect=False, bgcolor='w', show=True, save=False, close=True, file_format='png', filename='', dpi=300, annotate=False, node_color='#66ccff', node_size=15, node_alpha=1, node_edgecolor='none', node_zorder=1, edge_color='#999999', edge_linewidth=1, edge_alpha=1, use_geom=True):
    "\n    Plot a networkx spatial graph.\n    Parameters\n    ----------\n    G : networkx multidigraph\n    bbox : tuple\n        bounding box as north,south,east,west - if None will calculate from\n        spatial extents of data. if passing a bbox, you probably also want to\n        pass margin=0 to constrain it.\n    fig_height : int\n        matplotlib figure height in inches\n    fig_width : int\n        matplotlib figure width in inches\n    margin : float\n        relative margin around the figure\n    axis_off : bool\n        if True turn off the matplotlib axis\n    equal_aspect : bool\n        if True set the axis aspect ratio equal\n    bgcolor : string\n        the background color of the figure and axis\n    show : bool\n        if True, show the figure\n    save : bool\n        if True, save the figure as an image file to disk\n    close : bool\n        close the figure (only if show equals False) to prevent display\n    file_format : string\n        the format of the file to save (e.g., 'jpg', 'png', 'svg')\n    filename : string\n        the name of the file if saving\n    dpi : int\n        the resolution of the image file if saving\n    annotate : bool\n        if True, annotate the nodes in the figure\n    node_color : string\n        the color of the nodes\n    node_size : int\n        the size of the nodes\n    node_alpha : float\n        the opacity of the nodes\n    node_edgecolor : string\n        the color of the node's marker's border\n    node_zorder : int\n        zorder to plot nodes, edges are always 2, so make node_zorder 1 to plot\n        nodes beneath them or 3 to plot nodes atop them\n    edge_color : string\n        the color of the edges' lines\n    edge_linewidth : float\n        the width of the edges' lines\n    edge_alpha : float\n        the opacity of the edges' lines\n    use_geom : bool\n        if True, use the spatial geometry attribute of the edges to draw\n        geographically accurate edges, rather than just lines straight from node\n        to node\n    Returns\n    -------\n    fig, ax : tuple\n    "
    node_Xs = [float(x) for (_, x) in G.nodes(data='x')]
    node_Ys = [float(y) for (_, y) in G.nodes(data='y')]
    if (bbox is None):
        edges = graph_to_gdfs(G, nodes=False, fill_edge_geometry=True)
        (west, south, east, north) = edges.total_bounds
    else:
        (north, south, east, west) = bbox
    bbox_aspect_ratio = ((north - south) / (east - west))
    if (fig_width is None):
        fig_width = (fig_height / bbox_aspect_ratio)
    (fig, ax) = plt.subplots(figsize=(fig_width, fig_height), facecolor=bgcolor)
    ax.set_facecolor(bgcolor)
    start_time = time.time()
    lines = []
    for (u, v, data) in G.edges(keys=False, data=True):
        if (('geometry' in data) and use_geom):
            (xs, ys) = data['geometry'].xy
            lines.append(list(zip(xs, ys)))
        else:
            x1 = G.nodes[u]['x']
            y1 = G.nodes[u]['y']
            x2 = G.nodes[v]['x']
            y2 = G.nodes[v]['y']
            line = [(x1, y1), (x2, y2)]
            lines.append(line)
    lc = LineCollection(lines, colors=edge_color, linewidths=edge_linewidth, alpha=edge_alpha, zorder=2)
    ax.add_collection(lc)
    ax.scatter(node_Xs, node_Ys, s=node_size, c=node_color, alpha=node_alpha, edgecolor=node_edgecolor, zorder=node_zorder)
    margin_ns = ((north - south) * margin)
    margin_ew = ((east - west) * margin)
    ax.set_ylim(((south - margin_ns), (north + margin_ns)))
    ax.set_xlim(((west - margin_ew), (east + margin_ew)))
    xaxis = ax.get_xaxis()
    yaxis = ax.get_yaxis()
    xaxis.get_major_formatter().set_useOffset(False)
    yaxis.get_major_formatter().set_useOffset(False)
    if axis_off:
        ax.axis('off')
        ax.margins(0)
        ax.tick_params(which='both', direction='in')
        xaxis.set_visible(False)
        yaxis.set_visible(False)
        fig.canvas.draw()
    if equal_aspect:
        ax.set_aspect('equal')
        fig.canvas.draw()
    elif (G.graph['crs'] == default_crs):
        coslat = np.cos(((((min(node_Ys) + max(node_Ys)) / 2.0) / 180.0) * np.pi))
        ax.set_aspect((1.0 / coslat))
        fig.canvas.draw()
    if annotate:
        for (node, data) in G.nodes(data=True):
            ax.annotate(node, xy=(data['x'], data['y']))
    (fig, ax) = save_and_show(fig, ax, save, show, close, file_format, dpi, axis_off, filename=filename)
    return (fig, ax)
