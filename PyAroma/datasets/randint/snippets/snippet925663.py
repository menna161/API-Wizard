from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import collections
import math
import random
from mathematics_dataset.sample import number
from mathematics_dataset.sample import ops
from mathematics_dataset.util import combinatorics
import numpy as np
import six
from six.moves import zip
import sympy


def arithmetic(value, entropy, length=None, add_sub=True, mul_div=True):
    'Generates an arithmetic expression with a given value.\n\n  Args:\n    value: Target value (integer or rational).\n    entropy: Amount of randomness to use in generating expression.\n    length: Number of ops to use. If `None` then suitable length will be picked\n        based on entropy by sampling within the range\n        `length_range_for_entropy`.\n    add_sub: Whether to include addition and subtraction operations.\n    mul_div: Whether to include multiplication and division operations.\n\n  Returns:\n    Instance of `ops.Op` containing expression.\n  '
    assert isinstance(entropy, float)
    if (length is None):
        (min_length, max_length) = length_range_for_entropy(entropy)
        length = random.randint(min_length, max_length)
        entropy -= math.log10(((max_length - min_length) + 1))
    else:
        assert isinstance(length, int)
    entropy += (combinatorics.log_number_binary_trees(length) / math.log(10))
    value = sympy.sympify(value)
    sample_args = _SampleArgs(length, entropy)
    return _arithmetic(value, sample_args, add_sub, mul_div)
