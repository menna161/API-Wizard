from __future__ import division, print_function
import numpy as np
from scipy.stats import gamma, exponnorm


def irregular_sampling(T, N, rseed=None):
    '\n    Generates an irregularly sampled time vector by perturbating a \n    linearly spaced vector and latter deleting a certain number of \n    points\n    \n    Parameters\n    ----------\n    T: float\n        Time span of the vector, i.e. how long it is in time\n    N: positive integer\n        Number of samples of the resulting time vector\n    rseed: \n        Random seed to feed the random number generator\n        \n    Returns\n    -------\n    t_irr: ndarray\n        An irregulary sampled time vector\n        \n    '
    sampling_period = (T / float(N))
    N = int(N)
    np.random.seed(rseed)
    t = np.linspace(0, T, num=(5 * N))
    t[1:(- 1)] += ((sampling_period * 0.5) * np.random.randn(((5 * N) - 2)))
    P = np.random.permutation((5 * N))
    t_irr = np.sort(t[P[:N]])
    return t_irr
