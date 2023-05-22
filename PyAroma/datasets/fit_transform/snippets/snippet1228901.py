import numpy as np
import pandas as pd
from sklearn.preprocessing import binarize
from epistasis.mapping import EpistasisMap
from epistasis.models.base import BaseModel, use_sklearn
from epistasis.models.utils import XMatrixException, arghandler
from epistasis.models.linear import EpistasisLinearRegression
from gpmap import GenotypePhenotypeMap


def fit_transform(self, X=None, y=None, **kwargs):
    self.fit(X=X, y=y, **kwargs)
    ypred = self.predict(X=X)
    gpm = GenotypePhenotypeMap.read_dataframe(dataframe=self.gpm.data[(ypred == 1)], wildtype=self.gpm.wildtype, mutations=self.gpm.mutations)
    return gpm
