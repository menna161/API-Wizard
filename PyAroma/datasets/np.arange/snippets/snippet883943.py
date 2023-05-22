import sys, os
import tempfile
import argparse
from collections import Counter
import numpy as np
import networkx as nx
from scipy.stats import entropy


def portrait_divergence_weighted(G, H, bins=None, binedges=None):
    'Network portrait divergence between two weighted graphs.\n    \n    bins = width of bins in percentiles\n    binedges = vector of bin edges\n    bins and binedges are mutually exclusive\n    '
    paths_G = list(nx.all_pairs_dijkstra_path_length(G))
    paths_H = list(nx.all_pairs_dijkstra_path_length(H))
    if (binedges is None):
        if (bins is None):
            bins = 1
        UPL_G = set(_get_unique_path_lengths(G, paths=paths_G))
        UPL_H = set(_get_unique_path_lengths(H, paths=paths_H))
        unique_path_lengths = sorted(list((UPL_G | UPL_H)))
        binedges = np.percentile(unique_path_lengths, np.arange(0, 101, bins))
    BG = weighted_portrait(G, paths=paths_G, binedges=binedges)
    BH = weighted_portrait(H, paths=paths_H, binedges=binedges)
    return portrait_divergence(BG, BH)
