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


@composition.module(number.is_integer)
def evaluate(value, sample_args, context=None):
    'Entity for evaluating an integer-valued polynomial at a given point.'
    is_question = (context is None)
    if (context is None):
        context = composition.Context()
    (entropy, sample_args) = sample_args.peel()
    if (value is None):
        entropy_value = random.uniform(1, (1 + (entropy / 3)))
        entropy = max(0, (entropy - entropy_value))
        value = number.integer(entropy_value, signed=True)
    entropy_input = random.uniform(1, (1 + (entropy / 3)))
    entropy = max(0, (entropy - entropy_input))
    input_ = number.integer(entropy_input, signed=True)
    degree = random.randint(1, 3)
    entropies = (entropy * np.random.dirichlet(list(range(1, (degree + 1)))))
    target = value
    coeffs_reversed = []
    for (i, coeff_entropy) in enumerate(entropies):
        power = (degree - i)
        coeff = number.integer(coeff_entropy, signed=True)
        if (input_ != 0):
            coeff += int(round((target / (input_ ** power))))
        if ((coeff == 0) and (i == 0)):
            coeff += random.choice([(- 1), 1])
        coeffs_reversed.append(coeff)
        target -= (coeff * (input_ ** power))
    coeffs_reversed.append(target)
    coefficients = list(reversed(coeffs_reversed))
    (polynomial_entity, input_) = context.sample(sample_args, [composition.Polynomial(coefficients), input_])
    composed = polynomial_entity.handle.apply(input_.handle)
    if is_question:
        template = random.choice(_TEMPLATES)
        return example.Problem(question=example.question(context, template, composed=composed), answer=value)
    else:
        return composition.Entity(context=context, value=value, expression=composed, description='Let {self} be {composed}.', composed=composed)
