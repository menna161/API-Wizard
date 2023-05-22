import numpy as np
import re
import math
import warnings
from .units import angstrom_to_bohr, ev_to_hartree
from .band import Band
from copy import deepcopy
import fortranformat as ff
from functools import reduce


def x_axis(self, reciprocal_lattice=None):
    'Generate the x-axis values for a band-structure plot.\n\n        Returns an array of cumulative distances in reciprocal space between sequential k-points.\n\n        Args:\n            reciprocal_lattice (:obj:`np.array`, optional): 3x3 Cartesian reciprocal lattice.    \n                Default is ``None``. If no reciprocal lattice is provided, the returned x-axis\n                values will be sequential integers, giving even spacings between sequential\n                k-points.\n        \n        Returns:\n            (np.array): An array of x-axis values.\n \n        '
    if (reciprocal_lattice is not None):
        cartesian_k_points = np.array([k.cart_coords(reciprocal_lattice) for k in k_points])
        x_axis = [0.0]
        for i in range(1, len(cartesian_k_points)):
            dk = (cartesian_k_points[(i - 1)] - cartesian_k_points[i])
            mod_dk = np.sqrt(np.dot(dk, dk))
            x_axis.append((mod_dk + x_axis[(- 1)]))
        x_axis = np.array(x_axis)
    else:
        x_axis = np.arange(len(self._k_points))
    return x_axis
