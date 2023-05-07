import tensorflow as tf
import numpy as np
from dps import cfg
from dps.utils import Param, prime_factors
from dps.utils.tf import ConvNet, ScopedFunction, MLP, apply_mask_and_group_at_front, tf_shape, apply_object_wise


def addition_compact_logspace(left, right):
    batch_size = tf.shape(left)[0]
    n = right.shape[1]
    tensors = []
    to_add = tf.concat([left, ((- 100) * tf.ones((batch_size, (n - 1))))], axis=1)
    for i in range(n):
        tensors.append((to_add + right[(:, i:(i + 1))]))
        to_add = tf.manip.roll(to_add, shift=1, axis=1)
    return tf.reduce_logsumexp(tf.stack(tensors, axis=2), axis=2)
