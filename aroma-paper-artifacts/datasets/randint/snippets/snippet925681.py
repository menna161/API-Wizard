from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import math
import random
from mathematics_dataset.util import display
import numpy as np
import six
import sympy


def non_integer_decimal(entropy, signed):
    'Returns a random decimal; integer divided by random power of ten.\n\n  Guaranteed to be non-integer (i.e., numbers after the decimal point).\n\n  Args:\n    entropy: Float.\n    signed: Boolean. Whether to also return negative numbers.\n\n  Returns:\n    Non-integer decimal.\n  '
    while True:
        base = integer(entropy, signed)
        shift = random.randint(1, int(math.ceil(entropy)))
        divisor = (10 ** shift)
        if ((base % divisor) != 0):
            return display.Decimal(sympy.Rational(base, divisor))
