import numpy as np
import pandas as pd
import lmfit
from sklearn.base import BaseEstimator, RegressorMixin
from epistasis.stats import pearson
from ..mapping import EpistasisMap, encoding_to_sites
from .base import BaseModel
from epistasis.matrix import get_model_matrix
from .utils import arghandler


def fit_transform(self, X=None, y=None, **kwargs):
    'Same as calling fit in ensemble model.\n        '
    self.fit(X=X, y=y, **kwargs)
