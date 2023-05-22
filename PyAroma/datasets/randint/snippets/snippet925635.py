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


@composition.module(composition.is_polynomial)
def collect(value, sample_args, context=None):
    'Collect terms in an unsimplified polynomial.'
    is_question = (context is None)
    if (context is None):
        context = composition.Context()
    (entropy, sample_args) = sample_args.peel()
    if (value is None):
        (entropy_value, entropy) = (entropy * np.random.dirichlet([2, 3]))
        degrees = [random.randint(1, 3)]
        value = composition.Polynomial(polynomials.sample_coefficients(degrees, entropy_value))
    assert isinstance(value, composition.Polynomial)
    coefficients = value.coefficients
    all_coefficients_are_integer = True
    for coeff in coefficients.flat:
        if (not number.is_integer(coeff)):
            all_coefficients_are_integer = False
            break
    if all_coefficients_are_integer:
        coefficients = polynomials.expand_coefficients(coefficients, entropy)
    else:
        sample_args = composition.SampleArgs(sample_args.num_modules, (sample_args.entropy + entropy))
    num_variables = coefficients.ndim
    variables = [sympy.Symbol(context.pop()) for _ in range(num_variables)]
    unsimplified = polynomials.coefficients_to_polynomial(coefficients, variables)
    simplified = unsimplified.sympy().expand()
    if (not ops.number_constants(unsimplified)):
        unsimplified = ops.Add(unsimplified, ops.Constant(0))
    context.sample_by_replacing_constants(sample_args, unsimplified)
    if is_question:
        template = 'Collect the terms in {unsimplified}.'
        return example.Problem(question=example.question(context, template, unsimplified=unsimplified), answer=simplified)
    else:
        function_symbol = context.pop()
        function = sympy.Function(function_symbol)(*variables)
        return composition.Entity(context=context, value=value, handle=composition.FunctionHandle(function_symbol), expression=unsimplified, polynomial_variables=variables, description='Let {function} = {unsimplified}.', function=function, unsimplified=unsimplified)
