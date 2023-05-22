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


def sample_with_brackets(variables, degrees, entropy, length=None):
    'Constructs a polynomial with brackets.\n\n  Args:\n    variables: List of variables to use.\n    degrees: Max degrees of variables. This function guarantees that these will\n        be obtained in the returned polynomial.\n    entropy: Float >= 0; the randomness to use in generating the polynomial.\n    length: Optional integer containing number of terms. If `None` then an\n        appropriate one will be generated depending on the entropy.\n\n  Returns:\n    Instance of `ops.Op` containing the polynomial.\n  '
    if isinstance(degrees, int):
        degrees = [degrees]
    if (not isinstance(variables, (list, tuple))):
        variables = [variables]
    if (length is None):
        length = (3 + random.randint(0, int((entropy / 2))))
    entropy += (combinatorics.log_number_binary_trees(length) / math.log(10))
    return _sample_with_brackets(0, variables, degrees, entropy, length, True)
