from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import feature_map_constants as fmap_constants
import library_matching
import similarity as similarity_lib
import numpy as np
import tensorflow as tf


def _validate_permutation(perm1, perm2):
    ordered_indices = np.arange(perm1.shape[0])
    self.assertAllEqual(perm1[perm2], ordered_indices)
    self.assertAllEqual(perm2[perm1], ordered_indices)
