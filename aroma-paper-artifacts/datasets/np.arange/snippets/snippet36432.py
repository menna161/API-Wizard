import atexit
from concurrent.futures import ThreadPoolExecutor
from math import log, ceil
from tempfile import TemporaryFile
import numpy as np
import scipy
import time
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils import check_array, check_random_state, gen_batches
from sklearn.utils.validation import check_is_fitted
from modl.utils import get_sub_slice
from modl.utils.randomkit import RandomState
from modl.utils.randomkit import Sampler
from .dict_fact_fast import _enet_regression_multi_gram, _enet_regression_single_gram, _update_G_average, _batch_weight
from ..utils.math.enet import enet_norm, enet_projection, enet_scale


def transform(self, X):
    '\n        Compute the codes associated to input matrix X, decomposing it onto\n        the dictionary\n\n        Parameters\n        ----------\n        X: ndarray, shape = (n_samples, n_features)\n\n        Returns\n        -------\n        code: ndarray, shape = (n_samples, n_components)\n        '
    check_is_fitted(self, 'components_')
    dtype = self.components_.dtype
    X = check_array(X, order='C', dtype=dtype.type)
    if (X.flags['WRITEABLE'] is False):
        X = X.copy()
    (n_samples, n_features) = X.shape
    if ((not hasattr(self, 'G_agg')) or (self.G_agg != 'full')):
        G = self.components_.dot(self.components_.T)
    else:
        G = self.G_
    Dx = X.dot(self.components_.T)
    code = np.ones((n_samples, self.n_components), dtype=dtype)
    sample_indices = np.arange(n_samples)
    size_job = ceil((n_samples / self.n_threads))
    batches = list(gen_batches(n_samples, size_job))
    par_func = (lambda batch: _enet_regression_single_gram(G, Dx[batch], X[batch], code, get_sub_slice(sample_indices, batch), self.code_l1_ratio, self.code_alpha, self.code_pos, self.tol, self.max_iter))
    if (self.n_threads > 1):
        res = self._pool.map(par_func, batches)
        _ = list(res)
    else:
        _enet_regression_single_gram(G, Dx, X, code, sample_indices, self.code_l1_ratio, self.code_alpha, self.code_pos, self.tol, self.max_iter)
    return code
