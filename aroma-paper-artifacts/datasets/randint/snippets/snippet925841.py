from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import collections
import random
import string
from mathematics_dataset.sample import number
from mathematics_dataset.sample import ops
from mathematics_dataset.sample import polynomials
from mathematics_dataset.util import combinatorics
from mathematics_dataset.util import display
import numpy as np
import six
from six.moves import range
from six.moves import zip
import sympy


def sample_by_replacing_constants(self, sample_args, expressions):
    'Replaces some of the constants with handles from other modules.'
    max_children = (sample_args.num_modules - 1)
    if (max_children <= 0):
        return
    if isinstance(expressions, ops.Op):
        expressions = [expressions]
    constants = ops.number_constants(expressions)
    if (not constants):
        raise ValueError('No constants to replace in {}'.format([str(expr) for expr in expressions]))
    sample_count = random.randint(1, min(max_children, len(constants)))
    constants = random.sample(constants, sample_count)
    values = [constant.value for constant in constants]
    entities = self.sample(sample_args, values)
    for (constant, entity) in zip(constants, entities):
        constant.value = entity.handle
