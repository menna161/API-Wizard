from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import feature_map_constants as fmap_constants
import library_matching
import similarity as similarity_lib
import numpy as np
import tensorflow as tf


def testInvertPermutation(self):
    'Test library_matching._invert_permutation().'
    batch_size = 5
    num_trials = 10
    permutation_length = 6

    def _validate_permutation(perm1, perm2):
        ordered_indices = np.arange(perm1.shape[0])
        self.assertAllEqual(perm1[perm2], ordered_indices)
        self.assertAllEqual(perm2[perm1], ordered_indices)
    for _ in range(num_trials):
        perms = np.stack([np.random.permutation(permutation_length) for _ in range(batch_size)], axis=0)
        inverse = library_matching._invert_permutation(perms)
        for j in range(batch_size):
            _validate_permutation(perms[j], inverse[j])
