from itertools import count
import numpy as np
import pandas as pd
from numba import njit


@njit
def _compute_valid_splitting_indices(t, min_leaf):
    'Compute valid split indices for treatment array *t* given *min_leaf*.\n\n    Given an array *t* of treatment status and an integer *min_leaf* --denoting\n    the minimum number of allowed observations of each type in a leaf node--\n    computes a sequence of indices on which we can split *t* and get that each\n    resulting side contains a minimum of *min_leaf* treated and untreated\n    observations. Returns an empty sequence if no split is possible.\n\n    Args:\n        t (np.array): 1d array containing the treatment status as treated =\n            True and untreated = False.\n        min_leaf (int): Minimum number of observations of each type (treated,\n            untreated) allowed in a leaf; has to be greater than 1.\n\n    Returns:\n        out (np.array): a sequence of indices representing valid splitting\n            points.\n\n    '
    out = np.arange(0)
    n = len(t)
    if (n < (2 * min_leaf)):
        return out
    left_index_treated = np.argmax((np.cumsum(t) == min_leaf))
    if (left_index_treated == 0):
        return out
    left_index_untreated = np.argmax((np.cumsum((~ t)) == min_leaf))
    if (left_index_untreated == 0):
        return out
    tmparray = np.array([left_index_treated, left_index_untreated])
    left = np.max(tmparray)
    right_index_treated = np.argmax((np.cumsum(t[::(- 1)]) == min_leaf))
    if (right_index_treated == 0):
        return out
    right_index_untreated = np.argmax((np.cumsum((~ t[::(- 1)])) == min_leaf))
    if (right_index_untreated == 0):
        return out
    tmparray = np.array([right_index_treated, right_index_untreated])
    right = (n - np.max(tmparray))
    if (left > (right - 1)):
        return out
    else:
        out = np.arange(left, (right - 1))
        return out
