from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import collections
import functools
import random
from mathematics_dataset import example
from mathematics_dataset.modules import train_test_split
from mathematics_dataset.sample import number
from mathematics_dataset.util import composition
from mathematics_dataset.util import display
import six
import sympy


def _conversion_fraction(context, is_train):
    'E.g., "How many grams are in three quarters of a kg?".'
    dimension = random.choice(DIMENSIONS)
    allow_zero = (random.random() < 0.2)
    while True:
        (base_unit, target_unit) = random.sample(list(dimension.keys()), 2)
        base_value = number.non_integer_rational(2, signed=False)
        if (train_test_split.is_train(base_value) != is_train):
            continue
        answer = ((base_value * sympy.Rational(dimension[base_unit])) / sympy.Rational(dimension[target_unit]))
        if ((abs(answer) <= 100000) and (sympy.denom(answer) == 1) and (allow_zero or (answer != 0))):
            break
    template = random.choice(['How many {target_name} are there in {base_value} of a {base_name}?', 'What is {base_value} of a {base_name} in {target_name}?'])
    if ((sympy.denom(base_value) > 20) or random.choice([False, True])):
        base_value_string = base_value
    else:
        base_value_string = display.StringNumber(base_value)
    question = example.question(context, template, base_name=base_unit.name, base_value=base_value_string, target_name=pluralize(target_unit.name))
    return example.Problem(question=question, answer=answer)
