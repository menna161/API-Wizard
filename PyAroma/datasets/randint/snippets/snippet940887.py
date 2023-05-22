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


def _clean_sub_graphs(G_, min_length=80, max_nodes_to_skip=100, weight='length', verbose=True, super_verbose=False):
    "\n    Remove subgraphs with a max path length less than min_length,\n    if the subgraph has more than max_noxes_to_skip, don't check length\n       (this step great reduces processing time)\n    "
    if (len(G_.nodes()) == 0):
        return G_
    if verbose:
        print('Running clean_sub_graphs...')
    sub_graphs = list(nx.connected_component_subgraphs(G_))
    bad_nodes = []
    if verbose:
        print(' len(G_.nodes()):', len(G_.nodes()))
        print(' len(G_.edges()):', len(G_.edges()))
    if super_verbose:
        print('G_.nodes:', G_.nodes())
        edge_tmp = G_.edges()[np.random.randint(len(G_.edges()))]
        print(edge_tmp, 'G.edge props:', G_.edges[edge_tmp[0]][edge_tmp[1]])
    for G_sub in sub_graphs:
        if (len(G_sub.nodes()) > max_nodes_to_skip):
            continue
        else:
            all_lengths = dict(nx.all_pairs_dijkstra_path_length(G_sub, weight=weight))
            if super_verbose:
                print('  \nGs.nodes:', G_sub.nodes())
                print('  all_lengths:', all_lengths)
            lens = []
            for u in all_lengths.keys():
                v = all_lengths[u]
                for uprime in v.keys():
                    vprime = v[uprime]
                    lens.append(vprime)
                    if super_verbose:
                        print('  u, v', u, v)
                        print('    uprime, vprime:', uprime, vprime)
            max_len = np.max(lens)
            if super_verbose:
                print('  Max length of path:', max_len)
            if (max_len < min_length):
                bad_nodes.extend(G_sub.nodes())
                if super_verbose:
                    print(' appending to bad_nodes:', G_sub.nodes())
    G_.remove_nodes_from(bad_nodes)
    if verbose:
        print(' num bad_nodes:', len(bad_nodes))
        print(" len(G'.nodes()):", len(G_.nodes()))
        print(" len(G'.edges()):", len(G_.edges()))
    if super_verbose:
        print('  G_.nodes:', G_.nodes())
    return G_
