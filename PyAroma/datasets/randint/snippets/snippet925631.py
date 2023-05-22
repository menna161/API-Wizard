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


def coefficient_named(value, sample_args, context=None):
    'E.g., "Express x^2 + 2x in the form h * x^2 + k * x + t and give h.".'
    del value
    if (context is None):
        context = composition.Context()
    variable = sympy.Symbol(context.pop())
    (entropy, sample_args) = sample_args.peel()
    degree = random.randint(1, 4)
    if random.choice([False, True]):
        coefficients = polynomials.sample_coefficients(degree, (entropy / 2), min_non_zero=random.randint((degree - 1), degree))
        expanded = polynomials.expand_coefficients(coefficients, (entropy / 2))
        expression = polynomials.coefficients_to_polynomial(expanded, variable)
    else:
        expression = polynomials.sample_with_brackets(variable, degree, entropy)
        coefficients = list(reversed(sympy.Poly(expression).all_coeffs()))
    named_coeffs = [sympy.Symbol(context.pop()) for _ in range((degree + 1))]
    canonical = polynomials.coefficients_to_polynomial(named_coeffs, variable)
    if (random.random() < 0.2):
        power = random.randint(0, degree)
    else:
        non_zero_powers = [i for i in range((degree + 1)) if (coefficients[i] != 0)]
        power = random.choice(non_zero_powers)
    value = coefficients[power]
    named_coeff = named_coeffs[power]
    template = random.choice(['Express {expression} as {canonical} and give {target}.', 'Rearrange {expression} to {canonical} and give {target}.', 'Express {expression} in the form {canonical} and give {target}.', 'Rearrange {expression} to the form {canonical} and give {target}.'])
    return example.Problem(question=example.question(context, template, expression=expression, canonical=canonical, target=named_coeff), answer=value)
