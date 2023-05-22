import pathlib
import warnings
from copy import deepcopy
import numpy as np
import pandas as pd
from joblib import delayed
from joblib import Parallel
from cforest.tree import fit_causaltree
from cforest.tree import predict_causaltree


def _draw_feature_index(p, ratio, seed):
    'Draw random vector of feature indices.\n\n    Draw np.ceil(p * ratio) many indices from {0,...,p-1} without replacement.\n    We control the randomness by setting the seed to *seed*. If *ratio* = -1 we\n    return all indices {0,...,p-1} for debugging.\n\n    Args:\n        p (int): Number of features.\n        ratio (float): Ratio of features to draw, in [0, 1].\n        seed (int): Random number seed.\n\n    Returns:\n        indices (np.array): Index vector of length p.\n\n    '
    if (ratio == (- 1)):
        return np.arange(p)
    np.random.seed(seed)
    nfeat = int(np.ceil((p * ratio)))
    indices = np.random.choice(p, nfeat, replace=False)
    return indices
