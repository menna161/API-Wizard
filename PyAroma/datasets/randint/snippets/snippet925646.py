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


def _swr_space(is_train, sample_range):
    'Returns probability space for sampling without replacement.'
    num_sampled = random.randint(*sample_range)
    sample = _sample_letter_bag(is_train=is_train, min_total=num_sampled)
    space = probability.SampleWithoutReplacementSpace(sample.weights, num_sampled)
    random_variable = probability.FiniteProductRandomVariable(([sample.random_variable] * num_sampled))
    random_variable.description = ((str(display.StringNumber(num_sampled)) + ' letters picked without replacement from ') + sample.bag_contents)
    return (sample.letters_distinct, space, random_variable)
