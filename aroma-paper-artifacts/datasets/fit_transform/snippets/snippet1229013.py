import warnings
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, RegressorMixin
from gpmap import GenotypePhenotypeMap
from epistasis.mapping import EpistasisMap
from epistasis.models.base import BaseModel
from epistasis.models.utils import arghandler, FittingError
from epistasis.models.linear import EpistasisLinearRegression, EpistasisLasso
from epistasis.stats import pearson
from .minimizer import FunctionMinimizer


@arghandler
def fit_transform(self, X=None, y=None, **kwargs):
    self.fit(X=X, y=y, **kwargs)
    linear_phenotypes = self.transform(X=X, y=y)
    gpm = GenotypePhenotypeMap.read_dataframe(dataframe=self.gpm.data, wildtype=self.gpm.wildtype, mutations=self.gpm.mutations)
    gpm.data['phenotypes'] = linear_phenotypes
    return gpm
