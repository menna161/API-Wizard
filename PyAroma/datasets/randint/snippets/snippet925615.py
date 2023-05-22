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


def round_number(value, sample_args, context=None):
    'Question for rounding integers and decimals.'
    del value
    if (context is None):
        context = composition.Context()
    (entropy, sample_args) = sample_args.peel()
    power = random.randint((- 7), 6)
    answer_entropy = (1 + random.uniform(0, (entropy / 2)))
    entropy = max(1, (entropy - answer_entropy))
    value_integer = number.integer(answer_entropy, signed=True)
    remainder_divisor = (10 ** int(math.ceil(entropy)))
    remainder_range_lower = ((- remainder_divisor) / 2)
    remainder_range_upper = (remainder_divisor / 2)
    if (value_integer <= 0):
        remainder_range_lower += 1
    if (value_integer >= 0):
        remainder_range_upper -= 1
    remainder = random.randint(remainder_range_lower, remainder_range_upper)
    input_ = (value_integer + sympy.Rational(remainder, remainder_divisor))
    scale = ((10 ** power) if (power >= 0) else sympy.Rational(1, (10 ** (- power))))
    input_ = (input_ * scale)
    value = (value_integer * scale)
    if (not number.is_integer(input_)):
        input_ = display.Decimal(input_)
    if (not number.is_integer(value)):
        value = display.Decimal(value)
    (input_,) = context.sample(sample_args, [input_])
    if (power > 0):
        round_to = (10 ** power)
        if random.choice([False, True]):
            round_to = display.StringNumber(round_to, join_number_words_with_hyphens=False)
        description = 'the nearest {round_to}'.format(round_to=round_to)
    elif ((power == 0) and random.choice([False, True])):
        description = 'the nearest integer'
    else:
        description = random.choice(['{dps} decimal place', '{dps} dp'])
        if (power != (- 1)):
            description += 's'
        dps = (- power)
        if random.choice([False, True]):
            dps = display.StringNumber(dps)
        description = description.format(dps=dps)
    template = random.choice(['Round {input} to {description}.', 'What is {input} rounded to {description}?'])
    return example.Problem(question=example.question(context, template, input=input_, description=description), answer=value)
