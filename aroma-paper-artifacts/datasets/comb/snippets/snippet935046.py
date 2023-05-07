import numpy as np
from scipy.misc import comb


def bernstein_poly(i, n, t):
    '\n     The Bernstein polynomial of n, i as a function of t\n    '
    return ((comb(n, i) * (t ** (n - i))) * ((1 - t) ** i))
