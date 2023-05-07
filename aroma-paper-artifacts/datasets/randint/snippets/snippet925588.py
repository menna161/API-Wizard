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


def closest_count():
    lower = _closest_count_range(_ENTROPY_TRAIN[1])[1]
    return random.randint((lower + 1), (lower + _EXTRAPOLATION_EXTRA_COUNT))
