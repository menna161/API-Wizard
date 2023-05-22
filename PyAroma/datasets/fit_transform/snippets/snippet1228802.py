import json
import inspect
import numpy as np
import pandas as pd
from sklearn.preprocessing import binarize
from abc import abstractmethod, ABC, ABCMeta
from gpmap.gpm import GenotypePhenotypeMap
from epistasis.mapping import EpistasisMap, encoding_to_sites
from epistasis.matrix import get_model_matrix
from epistasis.utils import extract_mutations_from_genotypes, genotypes_to_X
from .utils import XMatrixException
from sklearn.base import RegressorMixin, BaseEstimator


@abstractmethod
def fit_transform(self, X=None, y=None, **kwargs):
    'Fit model to data and transform output according to model.\n\n        Parameters\n        ----------\n        X : None, ndarray, or list of genotypes. (default=None)\n            data used to construct X matrix that maps genotypes to\n            model coefficients. If None, the model uses genotypes in the\n            attached genotype-phenotype map. If a list of strings,\n            the strings are genotypes that will be converted to an X matrix.\n            If ndarray, the function assumes X is the X matrix used by the\n            epistasis model.\n\n        y : None or ndarray (default=None)\n            array of phenotypes. If None, the phenotypes in the attached\n            genotype-phenotype map is used.\n\n        Returns\n        -------\n        gpm : GenotypePhenotypeMap\n            The genotype-phenotype map object with transformed genotypes.\n        '
    raise SubclassException('Must be implemented in a subclass.')
