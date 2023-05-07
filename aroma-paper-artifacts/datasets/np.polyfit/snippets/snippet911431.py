import numpy as np
import re
import math
import warnings
from .units import angstrom_to_bohr, ev_to_hartree
from .band import Band
from copy import deepcopy
import fortranformat as ff
from functools import reduce


def least_squares_effective_mass(cartesian_k_points, eigenvalues):
    '\n    Calculate the effective mass using a least squares quadratic fit.\n\n    Args:\n        cartesian_k_points (np.array): Cartesian reciprocal coordinates for the k-points\n        eigenvalues (np.array):        Energy eigenvalues at each k-point to be used in the fit.\n\n    Returns:\n        (float): The fitted effective mass\n\n    Notes:\n        If the k-points do not sit on a straight line a ValueError will be raised.\n    '
    if (not points_are_in_a_straight_line(cartesian_k_points)):
        raise ValueError('k-points are not collinear')
    dk = (cartesian_k_points - cartesian_k_points[0])
    mod_dk = np.linalg.norm(dk, axis=1)
    delta_e = (eigenvalues - eigenvalues[0])
    effective_mass = (1.0 / ((np.polyfit(mod_dk, eigenvalues, 2)[0] * ev_to_hartree) * 2.0))
    return effective_mass
