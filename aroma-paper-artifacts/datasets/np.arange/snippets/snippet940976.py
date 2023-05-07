import os
import sys
import time
import numpy as np
import networkx as nx
import scipy.spatial
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection
from shapely.geometry import Point, LineString
import apls
import apls_plots
import apls_utils
import osmnx_funcs


def insert_holes_or_marbles(G_, origin_node, interval=50, n_id_add_val=1, verbose=False):
    '\n    Insert points on the graph on the specified interval\n    n_id_add_val sets min midpoint id above existing nodes\n        e.g.: G.nodes() = [1,2,4], if n_id_add_val = 5, midpoints will\n        be [9,10,11,...]\n    Apapted from apls.py.create_graph(midpoints()\n    '
    if (len(G_.nodes()) == 0):
        return (G_, [], [])
    (xms, yms) = ([], [])
    Gout = G_.copy()
    (midpoint_name_val, midpoint_name_inc) = ((np.max(list(G_.nodes())) + n_id_add_val), n_id_add_val)
    for (u, v, data) in G_.edges(data=True):
        if ('geometry' in data):
            edge_props_init = G_.edges([u, v])
            linelen = data['length']
            line = data['geometry']
            (xs, ys) = line.xy
            if (linelen < interval):
                continue
            if verbose:
                print('u,v:', u, v)
                print('data:', data)
                print('edge_props_init:', edge_props_init)
            interp_dists = np.arange(0, linelen, interval)[1:]
            if verbose:
                print('interp_dists:', interp_dists)
            node_id_new_list = []
            (xms_tmp, yms_tmp) = ([], [])
            for (j, d) in enumerate(interp_dists):
                if verbose:
                    print('j,d', j, d)
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
                    print('midpoint:', xm, ym)
                node_id = midpoint_name_val
                midpoint_name_val += midpoint_name_inc
                node_id_new_list.append(node_id)
                if verbose:
                    print('node_id:', node_id)
                (Gout, node_props, xn, yn) = apls.insert_point_into_G(Gout, point, node_id=node_id, allow_renaming=False, verbose=verbose)
    return (Gout, xms, yms)
