from datetime import datetime
import os
import re
import numpy as np
from scipy.interpolate import interp1d
from scipy.misc import derivative
import matplotlib.pyplot as plt


def gen_NACA4_airfoil(p, m, xx, n_points):
    '\n    Generate upper and lower points for a NACA 4 airfoil\n\n    Args:\n        :p:\n        :m:\n        :xx:\n        :n_points:\n\n    Returns:\n        :upper: 2 x N array with x- and y-coordinates of the upper side\n        :lower: 2 x N array with x- and y-coordinates of the lower side\n    '

    def yt(xx, xsi):
        a0 = 1.4845
        a1 = 0.63
        a2 = 1.758
        a3 = 1.4215
        a4 = 0.5075
        return (xx * (((((a0 * np.sqrt(xsi)) - (a1 * xsi)) - (a2 * (xsi ** 2))) + (a3 * (xsi ** 3))) - (a4 * (xsi ** 4))))

    def yc(p, m, xsi):

        def yc_xsi_lt_p(xsi):
            return ((m / (p ** 2)) * (((2 * p) * xsi) - (xsi ** 2)))

        def dyc_xsi_lt_p(xsi):
            return (((2 * m) / (p ** 2)) * (p - xsi))

        def yc_xsi_ge_p(xsi):
            return ((m / ((1 - p) ** 2)) * (((1 - (2 * p)) + ((2 * p) * xsi)) - (xsi ** 2)))

        def dyc_xsi_ge_p(xsi):
            return (((2 * m) / ((1 - p) ** 2)) * (p - xsi))
        yc = np.array([(yc_xsi_lt_p(x) if (x < p) else yc_xsi_ge_p(x)) for x in xsi])
        dyc = np.array([(dyc_xsi_lt_p(x) if (x < p) else dyc_xsi_ge_p(x)) for x in xsi])
        return (yc, dyc)
    xsi = np.linspace(0, 1, n_points)
    yt = yt(xx, xsi)
    (yc, dyc) = yc(p, m, xsi)
    theta = np.arctan(dyc)
    x_upper = (xsi - (yt * np.sin(theta)))
    y_upper = (yc + (yt * np.cos(theta)))
    x_lower = (xsi + (yt * np.sin(theta)))
    y_lower = (yc - (yt * np.cos(theta)))
    upper = np.array([x_upper, y_upper])
    lower = np.array([x_lower, y_lower])
    return (upper, lower)
