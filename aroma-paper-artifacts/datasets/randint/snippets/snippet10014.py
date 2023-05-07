import collections
from enum import Enum
from .state import State
import numpy as np


def init_random(size, k=2, n_randomized=None, empty_value=0, dtype=np.int):
    '\n    Returns a randomly initialized array with values consisting of numbers in {0,...,k - 1}, where k = 2 by default.\n    If dtype is not an integer type, then values will be uniformly distributed over the half-open interval [0, k - 1).\n    :param size: the size of the array to be created\n    :param k: the number of states in the Network Automaton (2, by default)\n    :param n_randomized: the number of randomized sites in the array; this value must be >= 0 and <= size, if specified;\n                         if this value is not specified, all sites in the array will be randomized; the randomized sites\n                         will be centered in the array, while all others will have an empty value\n    :param empty_value: the value to use for non-randomized sites (0, by default)\n    :param dtype: the data type\n    :return: a vector with shape (1, size), randomly initialized with numbers in {0,...,k - 1}\n    '
    if (n_randomized is None):
        n_randomized = size
    if ((n_randomized > size) or (n_randomized < 0)):
        raise Exception('the number of randomized sites, if specified, must be >= 0 and <= size')
    pad_left = ((size - n_randomized) // 2)
    pad_right = ((size - n_randomized) - pad_left)
    if np.issubdtype(dtype, np.integer):
        rand_nums = np.random.randint(k, size=n_randomized, dtype=dtype)
    else:
        rand_nums = np.random.uniform(0, (k - 1), size=n_randomized).astype(dtype)
    return np.array(np.pad(np.array(rand_nums), (pad_left, pad_right), 'constant', constant_values=empty_value)).tolist()
