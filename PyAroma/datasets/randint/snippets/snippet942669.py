import numpy as np
from tadataka.decorator import allow_1d


def random_binary(size):
    return np.random.randint(0, 2, size, dtype=np.bool)
