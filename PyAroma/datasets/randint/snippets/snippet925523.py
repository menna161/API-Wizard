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


def test_extra():
    'Returns dict of extrapolation testing modules.'
    sample_args_pure = composition.PreSampleArgs(1, 1, *_ENTROPY_EXTRAPOLATE)
    add_sub_sample_args_pure = composition.PreSampleArgs(1, 1, *_ADD_SUB_ENTROPY_EXTRAPOLATE)
    train_length = arithmetic.length_range_for_entropy(_ENTROPY_TRAIN[1])[1]

    def extrapolate_length():
        return random.randint((train_length + 1), (train_length + _EXTRAPOLATE_EXTRA_LENGTH))

    def add_sub_multiple_longer():
        return add_sub_multiple(_INT, sample_args_pure, length=extrapolate_length())

    def mul_div_multiple_longer():
        return mul_div_multiple(_INT, sample_args_pure, length=extrapolate_length())

    def mixed_longer():
        return mixed(_INT, sample_args_pure, length=extrapolate_length())
    return {'add_or_sub_big': functools.partial(add_or_sub, None, add_sub_sample_args_pure), 'mul_big': functools.partial(mul, None, sample_args_pure), 'div_big': functools.partial(div, None, sample_args_pure), 'add_sub_multiple_longer': add_sub_multiple_longer, 'mul_div_multiple_longer': mul_div_multiple_longer, 'mixed_longer': mixed_longer}
