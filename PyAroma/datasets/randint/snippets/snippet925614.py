from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import functools
import math
import random
from mathematics_dataset import example
from mathematics_dataset.sample import number
from mathematics_dataset.util import composition
from mathematics_dataset.util import display
import numpy as np
import six
from six.moves import range
import sympy


def place_value(value, sample_args, context=None):
    'E.g., "Q: What is the tens digit of 31859? A: 5.'
    del value
    if (context is None):
        context = composition.Context()
    (entropy, sample_args) = sample_args.peel()
    integer = number.integer(entropy, signed=False, min_abs=1)
    (entity,) = context.sample(sample_args, [integer])
    integer_as_string = str(integer)
    num_digits = len(integer_as_string)
    firsts = ['', 'ten ', 'hundred ']
    seconds = ['thousands', 'millions', 'billions', 'trillions', 'quadrillions', 'quintillions', 'sextillions', 'septillions', 'octillions', 'nonillions', 'decillions']
    place_names = ['units', 'tens', 'hundreds']
    for second in seconds:
        for first in firsts:
            place_names.append((first + second))
    place = random.randint(1, num_digits)
    place_name = place_names[(place - 1)]
    answer = sympy.Integer(integer_as_string[(num_digits - place)])
    return example.Problem(question=example.question(context, 'What is the {place_name} digit of {integer}?', place_name=place_name, integer=entity.expression_else_handle), answer=answer)
