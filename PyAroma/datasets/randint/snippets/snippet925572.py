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


def pair(sample_args, context=None):
    'Compares two numbers, e.g., "is 1/2 < 0.5?".'
    if (context is None):
        context = composition.Context()
    (entropy, sample_args) = sample_args.peel()

    def integers_close():
        (entropy_diff, entropy_left) = (entropy * np.random.dirichlet([1, 3]))
        left = number.integer(entropy_left, True)
        right = (left + number.integer(entropy_diff, True))
        return (left, right)

    def rational_and_integer():
        left = number.non_integer_rational(entropy, True)
        right = (int(round(left)) + random.randint((- 1), 1))
        return (left, right)

    def independent():
        (entropy_left, entropy_right) = (entropy * np.random.dirichlet([1, 1]))
        left = integer_or_rational_or_decimal(entropy_left)
        right = integer_or_rational_or_decimal(entropy_right)
        return (left, right)
    generator = random.choice([integers_close, rational_and_integer, independent])
    (left, right) = generator()
    if random.choice([False, True]):
        (left, right) = (right, left)
    (left, right) = context.sample(sample_args, [left, right])
    return _make_comparison_question(context, left, right)
