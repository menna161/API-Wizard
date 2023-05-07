from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import functools
import math
import random
from mathematics_dataset import example
from mathematics_dataset.sample import number
from mathematics_dataset.sample import ops
from mathematics_dataset.sample import polynomials
from mathematics_dataset.util import composition
import numpy as np
from six.moves import range
import sympy


def expand(value, sample_args, context=None):
    'E.g., "Expand (x**2 + 1)**2.".'
    del value
    if (context is None):
        context = composition.Context()
    variable = sympy.Symbol(context.pop())
    (entropy, sample_args) = sample_args.peel()
    min_order = 1
    max_order = 5
    order = random.randint(min_order, max_order)
    entropy -= math.log10(((max_order - min_order) + 1))
    expression_ = polynomials.sample_with_brackets(variable, order, entropy)
    expanded = sympy.expand(expression_)
    template = random.choice(['Expand {expression}.'])
    return example.Problem(question=example.question(context, template, expression=expression_), answer=expanded)
