import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
from scipy.stats import spearmanr, rankdata
from utils.torch import to_numpy
from common import N_TARGETS, TARGETS


def spearmanr_np(preds, targets, ix=None, ignore_hard_targets=False, optimized_rounding=False):
    ix = (ix if (ix is not None) else np.arange(preds.shape[0]))
    n_targets = (N_TARGETS - (ignore_hard_targets * len(hard_targets)))
    if optimized_rounding:
        preds = optimized_round(preds, targets, verbose=False, ix=ix)
    score = 0
    for (i, t) in enumerate(TARGETS):
        if (ignore_hard_targets and (t in hard_targets)):
            continue
        score_i = spearmanr(preds[(ix, i)], targets[(ix, i)]).correlation
        score += np.nan_to_num((score_i / n_targets))
    return score
