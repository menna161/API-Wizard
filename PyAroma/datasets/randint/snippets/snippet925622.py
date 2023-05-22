from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import functools
import math
import random
from mathematics_dataset import example
from mathematics_dataset.sample import number
from mathematics_dataset.util import composition
from mathematics_dataset.util import display
import numpy as np
import six
from six.moves import range
import sympy


def _random_coprime_pair(entropy):
    'Returns a pair of random coprime integers.'
    coprime_product = number.integer(entropy, False, min_abs=1)
    factors = sympy.factorint(coprime_product)

    def take():
        prime = random.choice(list(factors.keys()))
        power = factors[prime]
        del factors[prime]
        return (prime ** power)
    if ((random.random() < 0.8) and (len(factors) >= 2)):
        count_left = random.randint(1, (len(factors) - 1))
        count_right = (len(factors) - count_left)
    else:
        count_left = random.randint(0, len(factors))
        count_right = (len(factors) - count_left)
    left = sympy.prod([take() for _ in range(count_left)])
    right = sympy.prod([take() for _ in range(count_right)])
    assert ((left * right) == coprime_product)
    return (left, right)
