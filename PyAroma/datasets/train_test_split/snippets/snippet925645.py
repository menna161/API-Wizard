from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import collections
import functools
import random
import string
from mathematics_dataset import example
from mathematics_dataset.modules import train_test_split
from mathematics_dataset.util import combinatorics
from mathematics_dataset.util import composition
from mathematics_dataset.util import display
from mathematics_dataset.util import probability
import numpy as np
from six.moves import range
from six.moves import zip


def _sample_letter_bag(is_train, min_total):
    'Samples a "container of letters" and returns info on it.'
    while True:
        num_distinct_letters = random.randint(1, _MAX_DISTINCT_LETTERS)
        num_letters_total = random.randint(max(num_distinct_letters, min_total), min(_MAX_TOTAL_LETTERS, (num_distinct_letters * _MAX_LETTER_REPEAT)))
        letter_counts = combinatorics.uniform_positive_integers_with_sum(num_distinct_letters, num_letters_total)
        if ((is_train is None) or (train_test_split.is_train(sorted(letter_counts)) == is_train)):
            break
    letters_distinct = random.sample(_LETTERS, num_distinct_letters)
    weights = {i: 1 for i in range(num_letters_total)}
    letters_with_repetition = []
    for (letter, count) in zip(letters_distinct, letter_counts):
        letters_with_repetition += ([letter] * count)
    random.shuffle(letters_with_repetition)
    random_variable = probability.DiscreteRandomVariable({i: letter for (i, letter) in enumerate(letters_with_repetition)})
    if random.choice([False, True]):
        bag_contents = ''.join(letters_with_repetition)
    else:
        letters_and_counts = ['{}: {}'.format(letter, count) for (letter, count) in zip(letters_distinct, letter_counts)]
        bag_contents = (('{' + ', '.join(letters_and_counts)) + '}')
    return LetterBag(weights=weights, random_variable=random_variable, letters_distinct=letters_distinct, bag_contents=bag_contents)
