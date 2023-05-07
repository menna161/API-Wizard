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


def compose(value, sample_args, context=None):
    'E.g., "Let f(x)=2x+1, let g(x)=3x+10. What is f(g(x))?".'
    del value
    if (context is None):
        context = composition.Context()
    (entropy, sample_args) = sample_args.peel()
    (entropy_f, entropy_g) = (entropy * np.random.dirichlet([1, 1]))
    coeffs_f = polynomials.sample_coefficients([random.randint(1, 2)], entropy_f)
    coeffs_g = polynomials.sample_coefficients([random.randint(1, 2)], entropy_g)
    (entity_f, entity_g) = context.sample(sample_args, [composition.Polynomial(coeffs_f), composition.Polynomial(coeffs_g)])
    variable = sympy.var(context.pop())
    poly_f = polynomials.coefficients_to_polynomial(coeffs_f, variable)
    poly_g = polynomials.coefficients_to_polynomial(coeffs_g, variable)
    poly_f_g = poly_f.sympy().subs(variable, poly_g.sympy()).expand()
    expression = composition.FunctionHandle(entity_f, entity_g).apply(variable)
    template = random.choice(_TEMPLATES)
    return example.Problem(question=example.question(context, template, composed=expression), answer=poly_f_g)
