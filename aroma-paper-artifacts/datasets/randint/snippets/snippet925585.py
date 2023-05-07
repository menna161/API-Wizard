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


def closest(sample_args, count=None):
    'Ask for the closest to a given value in a list.'
    sample_args = sample_args()
    context = composition.Context()
    (entropy, sample_args) = sample_args.peel()
    if (count is None):
        count = random.randint(*_closest_count_range(entropy))
    display_multichoice = random.choice([False, True])
    if display_multichoice:
        _mark_choice_letters_used(count, context)
    (entropy_target, entropy_list) = (entropy * np.random.dirichlet([1, count]))
    target = integer_or_rational_or_decimal(entropy_target)
    while True:
        value_entropies = (entropy_list * np.random.dirichlet(np.ones(count)))
        value_entropies = np.maximum(1, value_entropies)
        values = [integer_or_rational_or_decimal(ent) for ent in value_entropies]
        differences = [abs((sympy.sympify(value) - target)) for value in values]
        if (len(sympy.FiniteSet(*differences)) == count):
            break
    target_and_entities = context.sample(sample_args, ([target] + values))
    target = target_and_entities[0]
    entities = target_and_entities[1:]
    min_difference = min(differences)
    answer_index = differences.index(min_difference)
    answer = entities[answer_index]
    adjective = random.choice(['closest', 'nearest'])
    if display_multichoice:
        return _closest_multichoice_question(context=context, entities=entities, target=target, adjective=adjective, answer=answer)
    else:
        return _closest_in_list_question(context=context, entities=entities, target=target, adjective=adjective, answer=answer)
