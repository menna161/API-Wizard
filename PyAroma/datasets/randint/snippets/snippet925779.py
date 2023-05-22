from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import math
import random
from mathematics_dataset.sample import number
from mathematics_dataset.sample import ops
from mathematics_dataset.util import combinatorics
import numpy as np
import six
from six.moves import range
from six.moves import zip
import sympy
from sympy.solvers.diophantine import base_solution_linear as diophantine_solve_linear_2d


def coefficients_linear_split(coefficients, entropy):
    'Finds two sets of coefficients and multipliers summing to `coefficients`.\n\n  Given `coefficients` (an integer vector), will sample integers `a, b`, and\n  two sets of coefficients `coefficients_1, coefficients_2`, such that\n  `a * coefficients_1 + b * coefficients_2 == coefficients`.\n\n  Args:\n    coefficients: Array of coefficients.\n    entropy: Float >= 0; the amount of randomness used to sample.\n\n  Returns:\n    Tuple (a, b, coefficients_1, coefficients_2)`.\n  '
    coefficients = np.asarray(coefficients)
    coefficients_shape = coefficients.shape
    coefficients = np.reshape(coefficients, [(- 1)])
    entropy_a = max(1, random.uniform(0, (entropy / 3)))
    entropy_b = max(1, random.uniform(0, (entropy / 3)))
    entropy -= (entropy_a + entropy_b)
    entropy_coefficients = (entropy * np.random.dirichlet(np.ones(len(coefficients))))
    coefficients_gcd = sympy.gcd([i for i in coefficients])
    coefficients_gcd = max(1, abs(coefficients_gcd))
    a = number.integer(entropy_a, signed=True, min_abs=1)
    b = number.integer(entropy_b, signed=True, min_abs=1, coprime_to=a)
    b *= _random_factor(coefficients_gcd)
    if random.choice([False, True]):
        (a, b) = (b, a)
    coefficients_1 = np.zeros(coefficients.shape, dtype=np.object)
    coefficients_2 = np.zeros(coefficients.shape, dtype=np.object)
    for (index, coefficient) in enumerate(coefficients):
        entropy_coeff = entropy_coefficients[index]
        t = number.integer(entropy_coeff, signed=True)
        (x, y) = diophantine_solve_linear_2d(c=coefficient, a=a, b=b, t=t)
        coefficients_1[index] = x
        coefficients_2[index] = y
    while (np.all((coefficients_1 == 0)) or np.all((coefficients_2 == 0))):
        index = random.randint(0, (len(coefficients) - 1))
        scale = random.choice([(- 1), 1])
        coefficients_1[index] += (scale * b)
        coefficients_2[index] -= (scale * a)
    coefficients_1 = np.reshape(coefficients_1, coefficients_shape)
    coefficients_2 = np.reshape(coefficients_2, coefficients_shape)
    return (a, b, coefficients_1, coefficients_2)
