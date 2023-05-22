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


def _unique_values(entropy, only_integers=False, count=None):
    'Generates unique values.'
    if (count is None):
        count = random.randint(*_sort_count_range(entropy))
    if only_integers:
        sampler = functools.partial(number.integer, signed=True)
    else:
        sampler = integer_or_rational_or_decimal
    for _ in range(1000):
        entropies = (entropy * np.random.dirichlet(np.ones(count)))
        entropies = np.maximum(1, entropies)
        values = [sampler(ent) for ent in entropies]
        if (len(sympy.FiniteSet(*values)) == len(values)):
            return values
    raise ValueError('Could not generate {} unique values with entropy={}'.format(count, entropy))
