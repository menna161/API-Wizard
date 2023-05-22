import sys, os
import tempfile
import argparse
from collections import Counter
import numpy as np
import networkx as nx
from scipy.stats import entropy


def portrait_divergence(G, H):
    'Compute the network portrait divergence between graphs G and H.'
    BG = _graph_or_portrait(G)
    BH = _graph_or_portrait(H)
    (BG, BH) = pad_portraits_to_same_size(BG, BH)
    (L, K) = BG.shape
    V = np.tile(np.arange(K), (L, 1))
    XG = ((BG * V) / (BG * V).sum())
    XH = ((BH * V) / (BH * V).sum())
    P = XG.ravel()
    Q = XH.ravel()
    M = (0.5 * (P + Q))
    KLDpm = entropy(P, M, base=2)
    KLDqm = entropy(Q, M, base=2)
    JSDpq = (0.5 * (KLDpm + KLDqm))
    return JSDpq
