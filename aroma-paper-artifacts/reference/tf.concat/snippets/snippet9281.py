import tensorflow as tf
import numpy as np


def all_pairs_tf(a, b):
    '\n    Return a tensor of all pairs\n    a -- [batch_size1, dim]\n    b -- [batch_size2, dim]\n    '
    dim = tf.shape(a)[1]
    temp_a = (tf.expand_dims(a, axis=1) + tf.zeros(tf.shape(tf.expand_dims(b, axis=0)), dtype=b.dtype))
    temp_b = (tf.zeros(tf.expand_dims(a, axis=1), dtype=a.dtype) + tf.expand_dims(b, axis=0))
    return tf.concat((tf.reshape(temp_a, [(- 1), 1, dim]), tf.reshape(temp_b, [(- 1), 1, dim])), axis=1)
