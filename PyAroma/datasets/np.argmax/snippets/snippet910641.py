import os
import random
import torch
import numpy as np
from time import time


def voting(preds, pref_ind=0):
    n_models = len(preds)
    n_test = len(preds[0])
    final_preds = []
    for i in range(n_test):
        cur_preds = [preds[k][i] for k in range(n_models)]
        (classes, counts) = np.unique(cur_preds, return_counts=True)
        if ((counts == max(counts)).sum() > 1):
            final_preds.append(preds[pref_ind][i])
        else:
            final_preds.append(classes[np.argmax(counts)])
    return final_preds
