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


def sample_degree(max_degree):
    'Select in range [0, max_degree], biased away from ends.'
    if ((max_degree <= 1) or random.choice([False, True])):
        return random.randint(0, max_degree)
    return random.randint(1, (max_degree - 1))
