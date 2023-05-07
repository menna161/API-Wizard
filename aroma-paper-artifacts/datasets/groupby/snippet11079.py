import pathlib
import warnings
from copy import deepcopy
import numpy as np
import pandas as pd
from joblib import delayed
from joblib import Parallel
from cforest.tree import fit_causaltree
from cforest.tree import predict_causaltree


def predict_causalforest(cforest, X, num_workers):
    'Predicts individual treatment effects for a causal forest.\n\n    Predicts individual treatment effects for new observed features *X*\n    on a fitted causal forest *cforest*. Predictions are made in parallel with\n    *num_workers* processes.\n\n    Args:\n        cforest (pd.DataFrame): Fitted causal forest represented in a multi-\n            index pd.DataFrame consisting of several fitted causal trees\n        X (np.array): 2d array of new observations for which we predict the\n            individual treatment effect.\n        num_workers (int): Number of workers for parallelization.\n\n    Returns:\n        predictions (np.array): 1d array of treatment predictions.\n\n    '
    num_trees = len(cforest.groupby(level=0))
    (n, _) = X.shape
    predictions = Parallel(n_jobs=num_workers)((delayed(predict_causaltree)(cforest.loc[i], X) for i in range(num_trees)))
    predictions = [arr.reshape((1, n)) for arr in predictions]
    predictions = np.concatenate(predictions, axis=0)
    predictions = predictions.mean(axis=0)
    return predictions
