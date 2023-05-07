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


def __call__(self):
    'Samples `SampleArgs`.'
    return SampleArgs(num_modules=random.randint(self.min_modules, self.max_modules), entropy=random.uniform(self.min_entropy, self.max_entropy))
