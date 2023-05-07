import tensorflow as tf
import numpy as np
from dps import cfg
from dps.utils import Param, prime_factors
from dps.utils.tf import ConvNet, ScopedFunction, MLP, apply_mask_and_group_at_front, tf_shape, apply_object_wise


def addition_compact(left, right):
    batch_size = tf.shape(left)[0]
    m = left.shape[1]
    n = right.shape[1]
    running_sum = tf.zeros((batch_size, ((m + n) - 1)))
    to_add = tf.concat([left, tf.zeros((batch_size, (n - 1)))], axis=1)
    for i in range(n):
        running_sum += (to_add * right[(:, i:(i + 1))])
        to_add = tf.manip.roll(to_add, shift=1, axis=1)
    return running_sum
