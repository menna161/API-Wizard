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


def add_or_sub_in_base(sample_args):
    'Module for addition and subtraction in another base.'
    context = composition.Context()
    (entropy, sample_args) = sample_args.peel()
    (entropy_p, entropy_q) = _entropy_for_pair(entropy)
    p = number.integer(entropy_p, signed=True)
    q = number.integer(entropy_q, signed=True)
    base = random.randint(2, 16)
    if random.choice([False, True]):
        answer = (p + q)
        template = 'In base {base}, what is {p} + {q}?'
    else:
        answer = (p - q)
        template = 'In base {base}, what is {p} - {q}?'
    return example.Problem(question=example.question(context, template, base=base, p=display.NumberInBase(p, base), q=display.NumberInBase(q, base)), answer=display.NumberInBase(answer, base))
