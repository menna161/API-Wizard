from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import functools
import random
from mathematics_dataset import example
from mathematics_dataset.sample import number
from mathematics_dataset.sample import ops
from mathematics_dataset.util import composition
from mathematics_dataset.util import display
import numpy as np
from six.moves import range
import sympy


def kth_biggest(sample_args, count=None):
    'Asks for the kth biggest value in a list.'
    sample_args = sample_args()
    context = composition.Context()
    (entropy, sample_args) = sample_args.peel()
    values = _unique_values(entropy, count=count)
    count = len(values)
    display_multichoice = random.choice([False, True])
    if display_multichoice:
        _mark_choice_letters_used(count, context)
    entities = context.sample(sample_args, values)
    sorted_entities = sorted(entities, key=_entity_sort_key)
    ordinal = random.randint(1, count)
    if random.choice([False, True]):
        answer = sorted_entities[(- ordinal)]
        adjective = 'biggest'
    else:
        answer = sorted_entities[(ordinal - 1)]
        adjective = 'smallest'
    if (ordinal > 1):
        adjective = ((str(display.StringOrdinal(ordinal)) + ' ') + adjective)
    if display_multichoice:
        return _kth_biggest_multichoice_question(context=context, entities=entities, adjective=adjective, answer=answer)
    else:
        return _kth_biggest_list_question(context=context, entities=entities, adjective=adjective, answer=answer)
