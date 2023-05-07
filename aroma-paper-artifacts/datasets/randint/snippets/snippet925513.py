from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import functools
import random
from mathematics_dataset import example
from mathematics_dataset.sample import linear_system
from mathematics_dataset.sample import number
from mathematics_dataset.sample import ops
from mathematics_dataset.sample import polynomials
from mathematics_dataset.util import composition
from mathematics_dataset.util import display
import numpy as np
from six.moves import range
import sympy


def __init__(self, variable, entropy, min_degree=1, max_degree=3):
    'Initializes a random polynomial sequence.\n\n    Args:\n      variable: Variable to use.\n      entropy: Entropy for polynomial coefficients.\n      min_degree: Minimum order of polynomial.\n      max_degree: Maximum order of polynomial.\n    '
    self._degree = random.randint(min_degree, max_degree)
    self._variable = variable
    polynomial = polynomials.sample_with_small_evaluation(variable=self._variable, degree=self._degree, max_abs_input=(self._degree + 2), entropy=entropy)
    self._sympy = polynomial.sympy()
