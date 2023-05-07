from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import functools
import math
import random
from mathematics_dataset import example
from mathematics_dataset.sample import polynomials
from mathematics_dataset.util import composition
from mathematics_dataset.util import display
import numpy as np
from six.moves import range
import sympy


def _generate_polynomial(num_variables, entropy, derivative_order, derivative_axis):
    'Returns polynomial.'
    degrees = np.random.randint(1, 4, [num_variables])
    degrees[derivative_axis] = np.random.randint(0, 4)
    coefficients = polynomials.sample_coefficients(degrees, entropy)
    assert (derivative_order > 0)
    degrees[derivative_axis] = (derivative_order - 1)
    extra_coefficients = polynomials.sample_coefficients(degrees, entropy)
    return np.concatenate([extra_coefficients, coefficients], axis=derivative_axis)
