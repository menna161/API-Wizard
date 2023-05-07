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


def _sample_with_brackets(depth, variables, degrees, entropy, length, force_brackets=True):
    'Internal recursive function for: constructs a polynomial with brackets.'
    if force_brackets:
        length = max(2, length)
    if ((not force_brackets) and (random.choice([False, True]) or (length < 2))):
        return sample(variables, degrees, entropy, length)
    length_left = random.randint(1, (length - 1))
    length_right = (length - length_left)
    (entropy_left, entropy_right) = (entropy * np.random.dirichlet([length_left, length_right]))
    if random.choice([False, True]):
        while True:
            left = _sample_with_brackets((depth + 1), variables, degrees, entropy_left, length_left, True)
            right = _sample_with_brackets((depth + 1), variables, degrees, entropy_right, length_right, False)
            if random.choice([False, True]):
                (left, right) = (right, left)
            result = ops.Add(left, right)
            all_ok = True
            for (variable, degree) in zip(variables, degrees):
                if (_degree_of_variable(result, variable) != degree):
                    all_ok = False
                    break
            if all_ok:
                return result
    else:

        def sample_with_zero_check(degrees_, entropy_, length_):
            while True:
                result = _sample_with_brackets((depth + 1), variables, degrees_, entropy_, length_, False)
                if ((degrees_.sum() > 0) or (not result.sympy().is_zero)):
                    return result
        degrees = np.asarray(degrees)

        def sample_degree(max_degree):
            'Select in range [0, max_degree], biased away from ends.'
            if ((max_degree <= 1) or random.choice([False, True])):
                return random.randint(0, max_degree)
            return random.randint(1, (max_degree - 1))
        degrees_left = np.array([sample_degree(degree) for degree in degrees])
        degrees_right = (degrees - degrees_left)
        left = sample_with_zero_check(degrees_left, entropy_left, length_left)
        right = sample_with_zero_check(degrees_right, entropy_right, length_right)
        return ops.Mul(left, right)
