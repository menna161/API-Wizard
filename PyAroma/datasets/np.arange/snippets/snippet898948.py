from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from collections import namedtuple
from os import path
import feature_map_constants as fmap_constants
import mass_spec_constants as ms_constants
import util
import numpy as np
import tensorflow as tf


def _invert_permutation(perm):
    'Convert an array of permutations to an array of inverse permutations.\n\n  Args:\n    perm: a [batch_size, num_iterms] int array where each column is a\n      permutation.\n  Returns:\n    A [batch_size, num_iterms] int array where each column is the\n    inverse permutation of the corresponding input column.\n  '
    output = np.empty(shape=perm.shape, dtype=perm.dtype)
    output[(np.arange(perm.shape[0])[(..., np.newaxis)], perm)] = np.arange(perm.shape[1])[(np.newaxis, ...)]
    return output
