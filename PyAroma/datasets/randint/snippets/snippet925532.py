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


def nearest_integer_root(sample_args):
    'E.g., "Calculate the cube root of 35 to the nearest integer.".'
    context = composition.Context()
    if random.choice([False, True]):
        one_over_exponent = random.randint(2, 3)
    else:
        one_over_exponent = random.randint(2, 10)
    (entropy, sample_args) = sample_args.peel()
    value = number.integer(entropy, signed=False)
    answer = int(round((value ** (1 / one_over_exponent))))
    templates = ['What is {value} to the power of 1/{one_over_exponent}, to the nearest integer?']
    if (one_over_exponent != 2):
        ordinal = str()
        templates += ['What is the {ordinal} root of {value} to the nearest integer?']
    if (one_over_exponent == 2):
        templates += ['What is the square root of {value} to the nearest integer?']
    elif (one_over_exponent == 3):
        templates += ['What is the cube root of {value} to the nearest integer?']
    template = random.choice(templates)
    ordinal = display.StringOrdinal(one_over_exponent)
    return example.Problem(question=example.question(context, template, value=value, ordinal=ordinal, one_over_exponent=one_over_exponent), answer=answer)
