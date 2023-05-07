from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import math
import tensorflow as tf
from thumt.layers.nn import linear


def split_heads(inputs, num_heads, name=None):
    ' Split heads\n    :param inputs: A tensor with shape [batch, ..., channels]\n    :param num_heads: An integer\n    :param name: An optional string\n    :returns: A tensor with shape [batch, heads, ..., channels / heads]\n    '
    with tf.name_scope(name, default_name='split_heads', values=[inputs]):
        x = inputs
        n = num_heads
        old_shape = x.get_shape().dims
        ndims = x.shape.ndims
        last = old_shape[(- 1)]
        new_shape = ((old_shape[:(- 1)] + [n]) + [((last // n) if last else None)])
        ret = tf.reshape(x, tf.concat([tf.shape(x)[:(- 1)], [n, (- 1)]], 0))
        ret.set_shape(new_shape)
        perm = (([0, (ndims - 1)] + [i for i in range(1, (ndims - 1))]) + [ndims])
        return tf.transpose(ret, perm)
