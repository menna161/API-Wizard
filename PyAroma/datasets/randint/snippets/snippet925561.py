from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import functools
import math
import random
from mathematics_dataset import example
from mathematics_dataset.sample import polynomials
from mathematics_dataset.util import composition
from mathematics_dataset.util import display
import numpy as np
from six.moves import range
import sympy


def _differentiate_polynomial(value, sample_args, context, num_variables):
    'Generates a question for differentiating a polynomial.'
    is_question = (context is None)
    if (context is None):
        context = composition.Context()
    if (value is not None):
        num_variables = value.coefficients.ndim
    (entropy, sample_args) = sample_args.peel()
    max_derivative_order = 3
    derivative_order = random.randint(1, max_derivative_order)
    entropy = max(0, (entropy - math.log10(max_derivative_order)))
    derivative_axis = random.randint(0, (num_variables - 1))
    if (value is None):
        coefficients = _generate_polynomial(num_variables, entropy, derivative_order, derivative_axis)
    else:
        coefficients = _sample_integrand(value.coefficients, derivative_order, derivative_axis, entropy)
    (entity,) = context.sample(sample_args, [composition.Polynomial(coefficients)])
    value = coefficients
    for _ in range(derivative_order):
        value = polynomials.differentiate(value, axis=derivative_axis)
    nth = display.StringOrdinal(derivative_order)
    if entity.has_expression():
        polynomial = entity.expression
        variables = entity.polynomial_variables
    else:
        variables = [sympy.Symbol(context.pop()) for _ in range(num_variables)]
        polynomial = entity.handle.apply(*variables)
    variable = variables[derivative_axis]
    if is_question:
        template = _template(context.module_count, derivative_order, len(variables))
        answer = polynomials.coefficients_to_polynomial(value, variables).sympy()
        return example.Problem(question=example.question(context, template, eq=polynomial, var=variable, nth=nth), answer=answer)
    else:
        fn_symbol = context.pop()
        variables_string = ', '.join((str(variable) for variable in variables))
        assert (len(variables) == 1)
        return composition.Entity(context=context, value=composition.Polynomial(value), description='Let {fn}({variables}) be the {nth} derivative of {eq}.', handle=composition.FunctionHandle(fn_symbol), fn=fn_symbol, variables=variables_string, nth=nth, eq=polynomial)
