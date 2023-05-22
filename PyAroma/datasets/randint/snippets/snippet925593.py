from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import functools
import random
from mathematics_dataset import example
from mathematics_dataset.sample import number
from mathematics_dataset.sample import ops
from mathematics_dataset.util import composition
from mathematics_dataset.util import display
import numpy as np
from six.moves import range
import sympy


def rational_and_integer():
    left = number.non_integer_rational(entropy, True)
    right = (int(round(left)) + random.randint((- 1), 1))
    return (left, right)
