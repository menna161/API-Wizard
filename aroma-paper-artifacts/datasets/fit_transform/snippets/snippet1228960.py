import numpy as np
from sklearn.linear_model import Lasso
from ..base import BaseModel, use_sklearn
from ..utils import arghandler
import warnings


def fit_transform(self, X=None, y=None, **kwargs):
    return self.fit(X=X, y=y, **kwargs)
