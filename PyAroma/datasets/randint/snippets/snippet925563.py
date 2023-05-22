from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import functools
import math
import random
from mathematics_dataset import example
from mathematics_dataset.sample import polynomials
from mathematics_dataset.util import composition
from mathematics_dataset.util import display
import numpy as np
from six.moves import range
import sympy


@composition.module(composition.is_polynomial)
def differentiate(value, sample_args, context=None):
    num_variables = random.randint(1, 4)
    return _differentiate_polynomial(value, sample_args, context, num_variables)
