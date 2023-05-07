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


@composition.module(composition.is_integer_polynomial)
def add(value, sample_args, context=None):
    'E.g., "Let f(x)=2x+1, g(x)=3x+2. What is 5*f(x) - 7*g(x)?".'
    is_question = (context is None)
    if (context is None):
        context = composition.Context()
    (entropy, sample_args) = sample_args.peel()
    if (value is None):
        max_degree = 3
        degree = random.randint(1, max_degree)
        entropy -= math.log10(max_degree)
        entropy_value = (entropy / 2)
        entropy -= entropy_value
        value = polynomials.sample_coefficients(degree, entropy=entropy_value, min_non_zero=random.randint(1, 3))
        value = composition.Polynomial(value)
    (c1, c2, coeffs1, coeffs2) = polynomials.coefficients_linear_split(value.coefficients, entropy)
    coeffs1 = polynomials.trim(coeffs1)
    coeffs2 = polynomials.trim(coeffs2)
    (c1, c2, fn1, fn2) = context.sample(sample_args, [c1, c2, composition.Polynomial(coeffs1), composition.Polynomial(coeffs2)])
    var = sympy.var(context.pop())
    expression = ((c1.handle * fn1.handle.apply(var)) + (c2.handle * fn2.handle.apply(var)))
    if is_question:
        answer = polynomials.coefficients_to_polynomial(value.coefficients, var)
        answer = answer.sympy()
        template = random.choice(_TEMPLATES)
        return example.Problem(question=example.question(context, template, composed=expression), answer=answer)
    else:
        intermediate_symbol = context.pop()
        intermediate = sympy.Function(intermediate_symbol)(var)
        return composition.Entity(context=context, value=value, description='Let {intermediate} = {composed}.', handle=composition.FunctionHandle(intermediate_symbol), intermediate=intermediate, composed=expression)
