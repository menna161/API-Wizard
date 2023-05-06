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


def prepare(self, n_samples=None, n_features=None, dtype=None, X=None):
    '\n        Init estimator attributes based on input shape and type.\n\n        Parameters\n        ----------\n        n_samples: int,\n\n        n_features: int,\n\n        dtype: dtype in np.float32, np.float64\n             to use in the estimator. Override X.dtype if provided\n        X: ndarray, shape (> n_components, n_features)\n            Array to use to determine shape and types, and init dictionary if\n            provided\n\n        Returns\n        -------\n        self\n        '
    if (X is not None):
        X = check_array(X, order='C', dtype=[np.float32, np.float64])
        if (dtype is None):
            dtype = X.dtype
        this_n_samples = X.shape[0]
        if (n_samples is None):
            n_samples = this_n_samples
        if (n_features is None):
            n_features = X.shape[1]
        elif (n_features != X.shape[1]):
            raise ValueError('n_features and X does not match')
    else:
        if ((n_features is None) or (n_samples is None)):
            raise ValueError('Either provideshape or data to function prepare.')
        if (dtype is None):
            dtype = np.float64
        elif (dtype not in [np.float32, np.float64]):
            return ValueError('dtype should be float32 or float64')
    if (self.optimizer not in ['variational', 'sgd']):
        return ValueError("optimizer should be 'variational' or 'sgd'")
    if (self.optimizer == 'sgd'):
        self.reduction = 1
        self.G_agg = 'full'
        self.Dx_agg = 'full'
    if (self.G_agg == 'average'):
        with TemporaryFile() as self.G_average_mmap_:
            self.G_average_mmap_ = TemporaryFile()
            self.G_average_ = np.memmap(self.G_average_mmap_, mode='w+', shape=(n_samples, self.n_components, self.n_components), dtype=dtype)
        atexit.register(self._exit)
    if (self.Dx_agg == 'average'):
        self.Dx_average_ = np.zeros((n_samples, self.n_components), dtype=dtype)
    self.C_ = np.zeros((self.n_components, self.n_components), dtype=dtype)
    self.B_ = np.zeros((self.n_components, n_features), dtype=dtype)
    self.gradient_ = np.zeros((self.n_components, n_features), dtype=dtype, order='F')
    self.random_state = check_random_state(self.random_state)
    if (X is None):
        self.components_ = np.empty((self.n_components, n_features), dtype=dtype)
        self.components_[(:, :)] = self.random_state.randn(self.n_components, n_features)
    else:
        self.components_ = check_array(X[:self.n_components], dtype=dtype.type, copy=True)
    if self.comp_pos:
        self.components_[(self.components_ <= 0)] = (- self.components_[(self.components_ <= 0)])
    for i in range(self.n_components):
        enet_scale(self.components_[i], l1_ratio=self.comp_l1_ratio, radius=1)
    self.code_ = np.ones((n_samples, self.n_components), dtype=dtype)
    self.labels_ = np.arange(n_samples)
    self.comp_norm_ = np.zeros(self.n_components, dtype=dtype)
    if (self.G_agg == 'full'):
        self.G_ = self.components_.dot(self.components_.T)
    self.n_iter_ = 0
    self.sample_n_iter_ = np.zeros(n_samples, dtype='int')
    self.random_state = check_random_state(self.random_state)
    random_seed = self.random_state.randint(MAX_INT)
    self.feature_sampler_ = Sampler(n_features, self.rand_size, self.replacement, random_seed)
    if self.verbose:
        self.verbose_iter_ = np.linspace(0, (n_samples * self.n_epochs), self.verbose).tolist()
    self.time_ = 0
    return self
