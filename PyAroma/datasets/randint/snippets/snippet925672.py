from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import random
from mathematics_dataset.sample import number
from mathematics_dataset.sample import ops
from mathematics_dataset.sample import polynomials
import numpy as np
from six.moves import range
import sympy


def linear_system(variables, solutions, entropy, non_trivial_in=None, length=None):
    'Returns a linear system (set of equalities) with the given solutions.\n\n  Args:\n    variables: List of variables.\n    solutions: List of solutions, of the same length as `variables`.\n    entropy: Float >= 0; the entropy used.\n    non_trivial_in: Optional integer corresponding to a variable for which the\n        solution shouldn\'t be "trivial". E.g., "solve a + b = 3, a = -2 for a"\n        is disallowed if `variables[non_trivial_in] == \'a\'`.\n    length: Total number of terms appearing; if `None` then selected wisely.\n\n  Returns:\n    List of `ops.Eq`.\n  '
    degree = len(variables)
    assert (degree == len(solutions))
    frac_entropy_matrix = random.uniform((1 / 3), (2 / 3))
    matrix = _invertible_matrix(degree, (entropy * frac_entropy_matrix), non_trivial_in)
    solutions = np.asarray(solutions)
    constant = np.matmul(matrix, solutions.astype(int))
    flattened = np.concatenate([np.reshape(matrix, [(degree * degree)]), constant])
    is_zero = (flattened == 0)
    if (length is None):
        min_length = (np.count_nonzero(flattened) + 1)
        max_length = max(min_length, (1 + int((degree * (1 + (entropy / 2))))))
        length = random.randint(min_length, max_length)
    counts = polynomials.expanded_coefficient_counts(length=length, is_zero=is_zero)
    entropies = (((1 - frac_entropy_matrix) * entropy) * np.random.dirichlet(np.maximum(1e-09, (counts - 1))))
    terms = []
    for i in range(len(flattened)):
        coeffs = polynomials.integers_with_sum(value=flattened[i], count=counts[i], entropy=entropies[i])
        terms.append(coeffs)
    matrix = terms[:(degree * degree)]
    constant = terms[(- degree):]
    equations = []
    for row_index in range(degree):
        monomials = []
        for col_index in range(degree):
            for term in matrix[((row_index * degree) + col_index)]:
                monomials.append(polynomials.monomial(term, variables[col_index], 1))
        for term in constant[row_index]:
            monomials.append(polynomials.monomial((- term), None, 0))
        equations.append(_make_equals_zero_split(monomials))
    return equations
