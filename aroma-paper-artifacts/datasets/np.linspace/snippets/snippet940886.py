import networkx as nx
import scipy.spatial
import scipy.stats
import numpy as np
import random
import utm
import copy
import matplotlib
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString
import time
import math
import os
import sys
import argparse
import pandas as pd
import shapely.wkt
import apls_utils
import apls_plots
import osmnx_funcs
import graphTools
import wkt_to_G
import topo_metric
import sp_metric


def create_graph_midpoints(G_, linestring_delta=50, is_curved_eps=0.03, n_id_add_val=1, allow_renaming=True, figsize=(0, 0), verbose=False, super_verbose=False):
    "\n    Insert midpoint nodes into long edges on the graph.\n\n    Arguments\n    ---------\n    G_ : networkx graph\n        Input networkx graph, with edges assumed to have a dictioary of\n        properties that includes the 'geometry' key.\n    linestring_delta : float\n        Distance in meters between linestring midpoints. Defaults to ``50``.\n    is_curved_eps : float\n        Minumum curvature for injecting nodes (if curvature is less than this\n        value, no midpoints will be injected). If < 0, always inject points\n        on line, regardless of curvature.  Defaults to ``0.3``.\n    n_id_add_val : int\n        Sets min midpoint id above existing nodes\n        e.g.: G.nodes() = [1,2,4], if n_id_add_val = 5, midpoints will\n        be [9,10,11,...]\n    allow_renameing : boolean\n        Switch to allow renaming of an existing node with node_id if the\n        existing node is closest to the point. Defaults to ``False``.\n    figsize : tuple\n        Figure size for optional plot. Defaults to ``(0,0)`` (no plot).\n    verbose : boolean\n        Switch to print relevant values to screen.  Defaults to ``False``.\n    super_verbose : boolean\n        Switch to print mucho values to screen.  Defaults to ``False``.\n\n    Returns\n    -------\n    Gout, xms, yms : tuple\n        Gout is the updated graph\n        xms, yms are coordinates of the inserted points\n    "
    if (len(G_.nodes()) == 0):
        return (G_, [], [])
    (xms, yms) = ([], [])
    Gout = G_.copy()
    (midpoint_name_val, midpoint_name_inc) = ((np.max(G_.nodes()) + n_id_add_val), 1)
    for (u, v, data) in G_.edges(data=True):
        if ('geometry' in data):
            edge_props_init = G_.edges([u, v])
            linelen = data['length']
            line = data['geometry']
            (xs, ys) = line.xy
            (minx, miny, maxx, maxy) = line.bounds
            dst = scipy.spatial.distance.euclidean([minx, miny], [maxx, maxy])
            if ((np.abs((dst - linelen)) / linelen) < is_curved_eps):
                continue
            if (linelen < (0.75 * linestring_delta)):
                continue
            if verbose:
                print('create_graph_midpoints()...')
                print('  u,v:', u, v)
                print('  data:', data)
                print('  edge_props_init:', edge_props_init)
            if (linelen <= linestring_delta):
                interp_dists = [(0.5 * line.length)]
            else:
                npoints = (len(np.arange(0, linelen, linestring_delta)) + 1)
                interp_dists = np.linspace(0, linelen, npoints)[1:(- 1)]
                if verbose:
                    print('  interp_dists:', interp_dists)
            node_id_new_list = []
            (xms_tmp, yms_tmp) = ([], [])
            for (j, d) in enumerate(interp_dists):
                if verbose:
                    print('    ', j, 'interp_dist:', d)
                midPoint = line.interpolate(d)
                (xm0, ym0) = midPoint.xy
                xm = xm0[(- 1)]
                ym = ym0[(- 1)]
                point = Point(xm, ym)
                xms.append(xm)
                yms.append(ym)
                xms_tmp.append(xm)
                yms_tmp.append(ym)
                if verbose:
                    print('    midpoint:', xm, ym)
                node_id = midpoint_name_val
                midpoint_name_val += midpoint_name_inc
                node_id_new_list.append(node_id)
                if verbose:
                    print('    node_id:', node_id)
                (Gout, node_props, _, _) = insert_point_into_G(Gout, point, node_id=node_id, allow_renaming=allow_renaming, verbose=super_verbose)
        if (figsize != (0, 0)):
            (fig, ax) = plt.subplots(1, 1, figsize=((1 * figsize[0]), figsize[1]))
            ax.plot(xs, ys, color='#6699cc', alpha=0.7, linewidth=3, solid_capstyle='round', zorder=2)
            ax.scatter(xm, ym, color='red')
            ax.set_title('Line Midpoint')
            plt.axis('equal')
    return (Gout, xms, yms)
