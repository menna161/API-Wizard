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


def sample_coefficients(degrees, entropy, min_non_zero=0, max_non_zero=None):
    'Generates grid of coefficients with shape `degrees + 1`.\n\n  This corresponds to univariate if degrees has length 1, otherwise\n  multivariate.\n\n  Args:\n    degrees: List of integers containing max degrees of variables.\n    entropy: Float >= 0; entropy for generating entries.\n    min_non_zero: Optional integer >= 1; the minimum number of non-zero coeffs.\n    max_non_zero: Optional integer >= 1; the maximum number of non-zero coeffs.\n\n  Returns:\n    NumPy int array of shape `degrees + 1`.\n  '
    if isinstance(degrees, int):
        degrees = [degrees]
    degrees = np.asarray(degrees)

    def random_index():
        return [random.randint(0, degrees[i]) for i in range(len(degrees))]
    indices = set()
    for (i, degree) in enumerate(degrees):
        if (degree > 0):
            index = random_index()
            index[i] = degree
            indices.add(tuple(index))
    abs_max_non_zero = np.prod((degrees + 1))
    min_non_zero = max(min_non_zero, 1, len(indices))
    if (max_non_zero is None):
        max_non_zero = (min_non_zero + int((entropy / 2)))
    min_non_zero = min(min_non_zero, abs_max_non_zero)
    max_non_zero = min(max_non_zero, abs_max_non_zero)
    max_non_zero = max(min_non_zero, max_non_zero)
    num_non_zero = random.randint(min_non_zero, max_non_zero)
    while (len(indices) < num_non_zero):
        indices.add(tuple(random_index()))
    coeffs = np.zeros((degrees + 1), dtype=np.int64)
    entropies = (entropy * np.random.dirichlet(np.ones(num_non_zero)))
    for (index, entry_entropy) in zip(indices, entropies):
        value = number.integer(entry_entropy, signed=True, min_abs=1)
        coeffs.itemset(index, value)
    return coeffs
