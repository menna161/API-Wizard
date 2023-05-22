import numpy as np


def rankArray(X):
    'Returns ranking of a list, with ties resolved by first-found first-order\n  NOTE: Sorts descending to follow numpy conventions\n  '
    tmp = np.argsort(X)
    rank = np.empty_like(tmp)
    rank[tmp] = np.arange(len(X))
    return rank
