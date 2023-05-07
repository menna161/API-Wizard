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


def base_conversion(min_entropy, max_entropy):
    'E.g., "What is 17 base 8 in base 10?".'
    context = composition.Context()
    from_base = random.randint(2, 16)
    while True:
        to_base = random.randint(2, 16)
        if (to_base != from_base):
            break
    entropy_used = math.log10((16 * 15))
    entropy = random.uniform((min_entropy - entropy_used), (max_entropy - entropy_used))
    value = number.integer(entropy, signed=True)
    template = random.choice(['{from_str} (base {from_base}) to base {to_base}', 'Convert {from_str} (base {from_base}) to base {to_base}.', 'What is {from_str} (base {from_base}) in base {to_base}?'])
    return example.Problem(question=example.question(context, template, from_str=display.NumberInBase(value, from_base), from_base=from_base, to_base=to_base), answer=display.NumberInBase(value, to_base))
