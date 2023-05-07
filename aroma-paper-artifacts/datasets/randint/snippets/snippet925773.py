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


def expand_coefficients(coefficients, entropy, length=None):
    'Expands coefficients to multiple terms that sum to each coefficient.\n\n  Args:\n    coefficients: Array, such that `coefficients[i, j, ..., k]` is the\n        coefficient of x**i * y**j * ... * z**k.\n    entropy: Float >= 0; the entropy to use for generating extra randomness.\n    length: Number of terms that appear, e.g., 2x + 3 has two terms. If `None`\n        then a suitable length will be picked depending on the entropy\n        requested.\n\n  Returns:\n    Numpy object array with the same shape as `coefficients`, containing lists.\n  '
    coefficients = np.asarray(coefficients)
    shape = coefficients.shape
    expanded_coefficients = np.empty(shape, dtype=np.object)
    min_length = (np.count_nonzero(coefficients) + 2)
    if (length is None):
        max_length = (min_length + int((math.ceil(entropy) / 2)))
        length = random.randint(min_length, max_length)
    if (length < min_length):
        length = min_length
    is_zero_flat = (np.reshape(coefficients, [(- 1)]) == 0)
    counts = expanded_coefficient_counts(length, is_zero=is_zero_flat)
    coeffs_entropy = (entropy * np.random.dirichlet(np.maximum(1e-09, (counts - 1))))
    counts = np.reshape(counts, shape)
    coeffs_entropy = np.reshape(coeffs_entropy, shape)
    indices = list(zip(*np.indices(shape).reshape([len(shape), (- 1)])))
    for power in indices:
        coeffs = integers_with_sum(value=coefficients.item(power), count=counts.item(power), entropy=coeffs_entropy.item(power))
        expanded_coefficients.itemset(power, coeffs)
    return expanded_coefficients
