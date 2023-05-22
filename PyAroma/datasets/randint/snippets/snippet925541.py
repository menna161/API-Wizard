from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import functools
import math
import random
from mathematics_dataset import example
from mathematics_dataset.sample import arithmetic
from mathematics_dataset.sample import number
from mathematics_dataset.sample import ops
from mathematics_dataset.util import composition
from mathematics_dataset.util import display
import sympy


def extrapolate_length():
    return random.randint((train_length + 1), (train_length + _EXTRAPOLATE_EXTRA_LENGTH))
