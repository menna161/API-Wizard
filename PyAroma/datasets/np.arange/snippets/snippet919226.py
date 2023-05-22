import numpy as np
from scipy.interpolate import interp1d


def lovenums(l):
    '\n    Estimate Load Love Numbers(LLNs). Intermediate numbers can be linearly interpolated with errors of less than \n    0.05% for all l<200, as opposed to direct calculation. Note: the first-degree LLNs is taken as 0.021.\n\n    Usage: \n    k_l =lovenums(l)\n\n    Inputs:\n    l -> [int, int list or array] Degree of LLNs \n\n    Outputs:\n    k_l -> [float, float array] LLNs for degree l\n        \n    Examples:\n    >>> k_l = lovenums(45)\n    >>> print(k_l)\n    -0.03\n    >>> k_ls = lovenums([45,58,96])\n    >>> print(k_ls)\n    [-0.03   -0.0242 -0.0148]\n    >>> k_ls = lovenums(np.arange(10,20))\n    >>> print(k_ls)\n    [-0.069  -0.0665 -0.064  -0.062  -0.06   -0.058  -0.0566 -0.0552 -0.0538 -0.0524]\n    '
    k_l_list = np.array([[0, 0.0], [1, 0.021], [2, (- 0.303)], [3, (- 0.194)], [4, (- 0.132)], [5, (- 0.104)], [6, (- 0.089)], [7, (- 0.081)], [8, (- 0.076)], [9, (- 0.072)], [10, (- 0.069)], [12, (- 0.064)], [15, (- 0.058)], [20, (- 0.051)], [30, (- 0.04)], [40, (- 0.033)], [50, (- 0.027)], [70, (- 0.02)], [100, (- 0.014)], [150, (- 0.01)], [200, (- 0.007)]])
    f = interp1d(k_l_list[(:, 0)], k_l_list[(:, 1)])
    k_l = f(l)
    return k_l
