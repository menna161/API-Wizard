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


def shuffle(self):
    '\n        Shuffle regression statistics, code_,\n        G_average_ and Dx_average_ and return the permutation used\n\n        Returns\n        -------\n        permutation: ndarray, shape = (n_samples)\n            Permutation used in shuffling regression statistics\n        '
    random_seed = self.random_state.randint(MAX_INT)
    random_state = RandomState(random_seed)
    list = [self.code_]
    if (self.G_agg == 'average'):
        list.append(self.G_average_)
    if (self.Dx_agg == 'average'):
        list.append(self.Dx_average_)
    perm = random_state.shuffle_with_trace(list)
    self.labels_ = self.labels_[perm]
    return perm
