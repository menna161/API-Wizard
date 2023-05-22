from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import functools
import random
from mathematics_dataset import example
from mathematics_dataset.sample import linear_system
from mathematics_dataset.sample import number
from mathematics_dataset.sample import ops
from mathematics_dataset.sample import polynomials
from mathematics_dataset.util import composition
from mathematics_dataset.util import display
import numpy as np
from six.moves import range
import sympy


def _sample_roots(entropy):
    'Generates `num_distinct + num_repeated` polynomial roots.'
    num_roots = random.randint(2, 5)
    num_repeated = np.random.binomial((num_roots - 1), _POLY_PROBABILITY_REPEATED_ROOT)
    if (entropy > 4):
        num_repeated = min(num_repeated, int((num_roots / 2)))
    num_distinct = (num_roots - num_repeated)
    entropies = (entropy * np.random.dirichlet(np.ones(num_distinct)))
    roots = []
    for root_entropy in entropies:
        if (random.random() < 0.1):
            root = number.non_integer_rational(root_entropy, True)
        else:
            root = number.integer(root_entropy, True)
        roots.append(root)
    for _ in range(num_repeated):
        roots.append(random.choice(roots[:num_distinct]))
    return roots
