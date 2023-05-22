from __future__ import division, print_function
import numpy as np
from scipy.stats import gamma, exponnorm


def power_law_noise(t, variance):
    '\n    CAUTION: NOT THOROUGHLY TESTED\n    Generates a red noise vector by first generating a covariance \n    function based on the expected red noise spectra. Red noise spectrum\n    follows a power law\n    \n        S(f) = A*f^(-2),\n    \n    where A is a constant. Pink noise can be obtained if the exponent is\n    changed to -1, and white noise if it is changed to 0.\n    \n    This Power Spectral density (PSD) is real and even then\n    \n        r(tau) = AT sum cos(2pi k tau/T)/k**2,\n    \n    where we assume f[k] = k*df, df = 1/T, Fs = N/T.\n    \n    The basel problem gives us: sum (1/k**2) approx pi**2/6, hence we can\n    set c according to the desired variance at lag=0\n     \n    After the covariance is computed we can draw from a multivariate\n    normal distribution to obtain a noise vector\n    \n    Parameters\n    ---------\n    t: ndarray\n        A time vector for which the red noise vector will be sampled\n    variance: positive float\n        variance of the resulting red noise vector\n        \n    Returns\n    -------\n    red_noise: ndarray\n        Vector containing the red noise realizations\n        \n    See also\n    --------\n    first_order_markov_process\n    \n    '
    if (variance < 0.0):
        raise ValueError('Variance must be positive')
    mu = np.zeros(shape=(N,))
    if (variance == 0.0):
        return mu
    N = len(t)
    T = (t[(- 1)] - t[0])
    c = ((6.0 * variance) / (T * (np.pi ** 2)))
    f = np.arange((1.0 / T), ((0.5 * N) / T), step=(1.0 / T))
    k = (f * T)
    dt = np.repeat(np.reshape(t, (1, (- 1))), N, axis=0)
    dt = np.absolute((dt - dt.T))
    S = np.zeros(shape=(N, N))
    for i in range(0, N):
        for j in range(i, N):
            S[(i, j)] = ((np.sum((np.cos(((((2.0 * np.pi) * k) * dt[(i, j)]) / T)) / (k ** 2))) * T) * c)
            S[(j, i)] = S[(i, j)]
    red_noise = np.random.multivariate_normal(mu, S)
    return red_noise
