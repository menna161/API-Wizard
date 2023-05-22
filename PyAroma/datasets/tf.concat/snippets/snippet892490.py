from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf


def maxout(inputs, output_size, maxpart=2, use_bias=True, concat=True, dtype=None, scope=None):
    "\n    Maxout layer\n    :param inputs: see the corresponding description of ``linear''\n    :param output_size: see the corresponding description of ``linear''\n    :param maxpart: an integer, the default value is 2\n    :param use_bias: a boolean value indicate whether to use bias term\n    :param concat: concat all tensors if inputs is a list of tensors\n    :param dtype: an optional instance of tf.Dtype\n    :param scope: the scope of this layer, the default value is ``maxout''\n    :returns: a Tensor with shape [batch, output_size]\n    :raises RuntimeError: see the corresponding description of ``linear''\n    "
    candidate = linear(inputs, (output_size * maxpart), use_bias, concat, dtype=dtype, scope=(scope or 'maxout'))
    shape = tf.concat([tf.shape(candidate)[:(- 1)], [output_size, maxpart]], axis=0)
    value = tf.reshape(candidate, shape)
    output = tf.reduce_max(value, (- 1))
    return output
