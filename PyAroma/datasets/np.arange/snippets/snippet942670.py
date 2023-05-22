import numpy as np
from tadataka.decorator import allow_1d


def indices_other_than(size, indices):
    '\n    size: size of the array you want to get elements from\n    example:\n    >>> indices_other_than(8, [1, 2, 3])\n    [0, 4, 5, 6, 7]\n    '
    return np.setxor1d(indices, np.arange(size))
