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


def _split_factors(integer):
    'Randomly factors integer into product of two integers.'
    assert integer.is_Integer
    if (integer == 0):
        return [1, 0]
    factors = sympy.factorint(integer)
    left = sympy.Integer(1)
    right = sympy.Integer(1)
    for (factor, mult) in six.iteritems(factors):
        left_mult = random.randint(0, mult)
        right_mult = (mult - left_mult)
        left *= (factor ** left_mult)
        right *= (factor ** right_mult)
    return (left, right)
