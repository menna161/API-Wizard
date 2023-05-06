import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from scipy.stats import spearmanr, rankdata
from utils.torch import to_numpy
from common import N_TARGETS, TARGETS


def optimize_rounding_params(oofs, y, verbose=True, ix=None):
    ix = (ix if (ix is not None) else np.arange(oofs.shape[0]))
    opt_ds = []
    opt_indices = []
    for idx in range(N_TARGETS):
        scores = [np.nan_to_num(spearmanr(scale(oofs[(ix, idx)], d), y[(ix, idx)])[0]) for d in ds]
        opt_d = ds[np.argmax(scores)]
        if ((np.max(scores) - spearmanr(oofs[(ix, idx)], y[(ix, idx)])[0]) > 0.002):
            if verbose:
                print(idx, opt_d, np.max(scores))
            opt_ds.append(opt_d)
            opt_indices.append(idx)
    return (opt_ds, opt_indices)
