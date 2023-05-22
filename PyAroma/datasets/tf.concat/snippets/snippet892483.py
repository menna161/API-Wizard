from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import math
import tensorflow as tf
from thumt.layers.nn import linear


def combine_heads(inputs, name=None):
    ' Combine heads\n    :param inputs: A tensor with shape [batch, heads, length, channels]\n    :param name: An optional string\n    :returns: A tensor with shape [batch, length, heads * channels]\n    '
    with tf.name_scope(name, default_name='combine_heads', values=[inputs]):
        x = inputs
        x = tf.transpose(x, [0, 2, 1, 3])
        old_shape = x.get_shape().dims
        (a, b) = old_shape[(- 2):]
        new_shape = (old_shape[:(- 2)] + [((a * b) if (a and b) else None)])
        x = tf.reshape(x, tf.concat([tf.shape(x)[:(- 2)], [(- 1)]], 0))
        x.set_shape(new_shape)
        return x
