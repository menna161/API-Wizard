from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import math
import random
from mathematics_dataset.util import display
import numpy as np
import six
import sympy


def integer(entropy, signed, min_abs=0, coprime_to=1):
    'Returns an integer from a set of size ceil(10**entropy).\n\n  If `signed` is True, then includes negative integers, otherwise includes just\n  positive integers.\n\n  Args:\n    entropy: Float >= 0.\n    signed: Boolean. Whether to also return negative numbers.\n    min_abs: Integer >= 0. The minimum absolute value.\n    coprime_to: Optional integer >= 1. The returned integer is guaranteed to be\n        coprime to `coprime_to`, with entropy still accounted for.\n\n  Returns:\n    Integer.\n  '
    assert (isinstance(min_abs, int) and (not isinstance(min_abs, bool)))
    coprime_to = abs(coprime_to)
    assert (min_abs >= 0)
    max_ = math.pow(10, entropy)
    max_ += min_abs
    if (coprime_to >= 2):
        max_ = ((max_ / _coprime_density(coprime_to)) + 1)
    if signed:
        max_ = int(math.ceil((max_ / 2)))
        range_ = [(- max_), max_]
    else:
        max_ = int(math.ceil(max_))
        range_ = [min_abs, max_]
    while True:
        value = random.randint(*range_)
        if ((abs(value) >= min_abs) and (sympy.gcd(value, coprime_to) == 1)):
            break
    return sympy.Integer(value)
