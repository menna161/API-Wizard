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


def is_factor(value, sample_args, context=None):
    'E.g., "Is 5 a factor of 48?".'
    del value
    if (context is None):
        context = composition.Context()
    (entropy, sample_args) = sample_args.peel()
    entropy_factor = (1 + random.uniform(0, (entropy / 3)))
    entropy = max(0, (entropy - entropy_factor))
    maybe_factor = number.integer(entropy_factor, False, min_abs=2)
    integer = (maybe_factor * number.integer(entropy, False, min_abs=1))
    if random.choice([False, True]):
        integer += random.randint(1, (maybe_factor - 1))
    (entity,) = context.sample(sample_args, [integer])
    templates = ['Is {maybe_factor} a factor of {value}?', 'Is {value} a multiple of {maybe_factor}?', 'Does {maybe_factor} divide {value}?']
    if (maybe_factor == 2):
        templates += ['Is {value} even?']
    template = random.choice(templates)
    answer = ((integer % maybe_factor) == 0)
    return example.Problem(question=example.question(context, template, maybe_factor=maybe_factor, value=entity.expression_else_handle), answer=answer)
