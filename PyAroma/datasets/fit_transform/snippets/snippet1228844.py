import numpy as np
from ..stats import pearson
from .base import BaseModel
from .utils import arghandler


def fit(self, X=None, y=None):
    'Fit pipeline.\n\n        Parameters\n        ----------\n        X : array\n            array of genotypes.\n\n        y : array\n            array of phentoypes.\n        '
    model = self[0]
    gpm = model.fit_transform(X=X, y=y)
    for model in self[1:]:
        model.add_gpm(gpm)
        try:
            gpm = model.fit_transform(X=X, y=y)
        except Exception as e:
            print('Failed with {}'.format(model))
            print('Input was :')
            print('X : {}'.format(X), print('y : {}'.format(y)))
            raise e
    return self
