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


def test_extra():
    'Returns dict of extrapolation testing modules.'
    sample_args_pure = composition.PreSampleArgs(1, 1, *_ENTROPY_EXTRAPOLATE)

    def sort_count():
        lower = _sort_count_range(_ENTROPY_TRAIN[1])[1]
        return random.randint((lower + 1), (lower + _EXTRAPOLATION_EXTRA_COUNT))

    def closest_count():
        lower = _closest_count_range(_ENTROPY_TRAIN[1])[1]
        return random.randint((lower + 1), (lower + _EXTRAPOLATION_EXTRA_COUNT))

    def kth_biggest_more():
        return kth_biggest(sample_args_pure, count=sort_count())

    def sort_more():
        return sort(sample_args_pure, count=sort_count())

    def closest_more():
        return closest(sample_args_pure, count=closest_count())
    return {'kth_biggest_more': kth_biggest_more, 'sort_more': sort_more, 'closest_more': closest_more}
