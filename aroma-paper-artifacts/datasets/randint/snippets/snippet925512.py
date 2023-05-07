from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import functools
import random
from mathematics_dataset import example
from mathematics_dataset.sample import linear_system
from mathematics_dataset.sample import number
from mathematics_dataset.sample import ops
from mathematics_dataset.sample import polynomials
from mathematics_dataset.util import composition
from mathematics_dataset.util import display
import numpy as np
from six.moves import range
import sympy


def sequence_nth_term(min_entropy, max_entropy):
    'E.g., "What is the nth term in the sequence 1, 2, 3?".'
    entropy = random.uniform(min_entropy, max_entropy)
    context = composition.Context()
    variable = sympy.Symbol(context.pop())
    sequence = _PolynomialSequence(variable, entropy)
    min_num_terms = sequence.min_num_terms
    num_terms = random.randint(min_num_terms, (min_num_terms + 3))
    sequence_sample = [sequence.term((n + 1)) for n in range(num_terms)]
    sequence_sample = display.NumberList(sequence_sample)
    template = random.choice(["What is the {variable}'th term of {sequence}?"])
    answer = sequence.sympy
    return example.Problem(question=example.question(context, template, variable=variable, sequence=sequence_sample), answer=answer)
