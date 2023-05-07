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


def _random_factor(integer):
    factors = sympy.factorint(integer)
    result = 1
    for (factor, power) in six.iteritems(factors):
        result *= (factor ** random.randint(0, power))
    return result
