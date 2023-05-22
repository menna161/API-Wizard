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


def _conversion_decimal(context, is_train, is_extrapolation):
    'E.g., "How many grams are in 5kg?".'
    dimension = random.choice(DIMENSIONS)
    while True:
        (base_value, base_unit, target_value, target_unit) = _sample_conversion_decimal(dimension, is_extrapolation)
        if (train_test_split.is_train(base_value) == is_train):
            break
    templates = ['How many {target_name} are there in {base_value} {base_name}?', 'What is {base_value} {base_name} in {target_name}?', 'Convert {base_value} {base_name} to {target_name}.']
    if (base_unit.symbol is not None):
        templates += ['How many {target_name} are there in {base_value}{base_symbol}?', 'What is {base_value}{base_symbol} in {target_name}?', 'Convert {base_value}{base_symbol} to {target_name}.']
    template = random.choice(templates)
    base_name = pluralize(base_unit.name)
    target_name = pluralize(target_unit.name)
    question = example.question(context, template, base_name=base_name, base_symbol=base_unit.symbol, base_value=base_value, target_name=target_name)
    return example.Problem(question=question, answer=target_value)
