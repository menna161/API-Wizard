import numpy as np
import scipy.integrate as integrate


def E0_sum(N, g):
    ks = (((np.linspace(((- (N - 1)) / 2), ((N - 1) / 2), num=N) / N) * 2) * np.pi)
    epsilon_ks = (2 * np.sqrt((((g ** 2) - ((2 * g) * np.cos(ks))) + 1)))
    E0 = (((- 0.5) * epsilon_ks.sum()) / N)
    return E0
