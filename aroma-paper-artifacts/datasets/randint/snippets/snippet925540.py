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


def simplify_surd(value, sample_args, context=None):
    'E.g., "Simplify (2 + 5*sqrt(3))**2.".'
    del value
    if (context is None):
        context = composition.Context()
    (entropy, sample_args) = sample_args.peel()
    while True:
        base = random.randint(2, 20)
        if sympy.Integer(base).is_prime:
            break
    num_primes_less_than_20 = 8
    entropy -= math.log10(num_primes_less_than_20)
    exp = _sample_surd(base, entropy, max_power=2, multiples_only=False)
    simplified = sympy.expand(sympy.simplify(exp))
    template = random.choice(['Simplify {exp}.'])
    return example.Problem(question=example.question(context, template, exp=exp), answer=simplified)
