from datetime import datetime
import os
import re
import numpy as np
from scipy.interpolate import interp1d
from scipy.misc import derivative
import matplotlib.pyplot as plt


@classmethod
def morph_new_from_two_foils(cls, airfoil1, airfoil2, eta, n_points):
    '\n        Create an airfoil object from a linear interpolation between two\n        airfoil objects\n\n        Note:\n            * This is an alternative constructor method\n\n        Args:\n            :airfoil1: Airfoil object at eta = 0\n            :airfoil2: Airfoil object at eta = 1\n            :eta: Relative position where eta = [0, 1]\n            :n_points: Number of points for new airfoil object\n\n        Returns:\n            :airfoil: New airfoil instance\n        '
    if (not (0 <= eta <= 1)):
        raise ValueError(f"'eta' must be in range [0,1], given eta is {float(eta):.3f}")
    x = np.linspace(0, 1, n_points)
    y_upper_af1 = airfoil1.y_upper(x)
    y_lower_af1 = airfoil1.y_lower(x)
    y_upper_af2 = airfoil2.y_upper(x)
    y_lower_af2 = airfoil2.y_lower(x)
    y_upper_new = ((y_upper_af1 * (1 - eta)) + (y_upper_af2 * eta))
    y_lower_new = ((y_lower_af1 * (1 - eta)) + (y_lower_af2 * eta))
    upper = np.array([x, y_upper_new])
    lower = np.array([x, y_lower_new])
    return cls(upper, lower)
