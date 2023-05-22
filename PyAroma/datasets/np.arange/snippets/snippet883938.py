import sys, os
import tempfile
import argparse
from collections import Counter
import numpy as np
import networkx as nx
from scipy.stats import entropy


def weighted_portrait(G, paths=None, binedges=None):
    "Compute weighted portrait of G, using Dijkstra's algorithm for finding\n    shortest paths. G is a networkx object.\n    \n    Return matrix B where B[i,j] is the number of starting nodes in graph with\n    j nodes at distance d_i <  d < d_{i+1}.\n    "
    if (paths is None):
        paths = list(nx.all_pairs_dijkstra_path_length(G))
    if (binedges is None):
        unique_path_lengths = _get_unique_path_lengths(G, paths=paths)
        sampled_path_lengths = np.percentile(unique_path_lengths, np.arange(0, 101, 1))
    else:
        sampled_path_lengths = binedges
    UPL = np.array(sampled_path_lengths)
    l_s_v = []
    for (i, (s, dist_dict)) in enumerate(paths):
        distances = np.array(list(dist_dict.values()))
        (s_v, e) = np.histogram(distances, bins=UPL)
        l_s_v.append(s_v)
    M = np.array(l_s_v)
    B = np.zeros(((len(UPL) - 1), (G.number_of_nodes() + 1)))
    for i in range((len(UPL) - 1)):
        col = M[(:, i)]
        for (n, c) in Counter(col).items():
            B[(i, n)] += c
    return B
