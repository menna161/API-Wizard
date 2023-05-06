import pathlib
import warnings
from copy import deepcopy
import numpy as np
import pandas as pd
from joblib import delayed
from joblib import Parallel
from cforest.tree import fit_causaltree
from cforest.tree import predict_causaltree


def _draw_resample_index(n, seed):
    'Compute vector of randomly drawn indices with replacement.\n\n    Draw indices with replacement from the discrete uniform distribution\n    on {0,...,n-1}. We control the randomness by setting the seed to *seed*.\n    If *seed* = -1 we return all indices {0,...,n-1} for debugging.\n\n    Args:\n        n (int): Upper bound for indices and number of indices to draw\n        seed (int): Random number seed.\n\n    Returns:\n        indices (np.array): Resample indices.\n\n    '
    if (seed == (- 1)):
        return np.arange(n)
    np.random.seed(seed)
    indices = np.random.randint(0, n, n)
    return indices
