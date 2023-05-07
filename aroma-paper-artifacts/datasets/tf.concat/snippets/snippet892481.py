from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import math
import tensorflow as tf
from thumt.layers.nn import linear


def add_timing_signal(x, min_timescale=1.0, max_timescale=10000.0, name=None):
    "\n    This function adds a bunch of sinusoids of different frequencies to a\n    Tensor. See paper: `Attention is all you need'\n\n    :param x: A tensor with shape [batch, length, channels]\n    :param min_timescale: A floating point number\n    :param max_timescale: A floating point number\n    :param name: An optional string\n\n    :returns: a Tensor the same shape as x.\n    "
    with tf.name_scope(name, default_name='add_timing_signal', values=[x]):
        length = tf.shape(x)[1]
        channels = tf.shape(x)[2]
        position = tf.to_float(tf.range(length))
        num_timescales = (channels // 2)
        log_timescale_increment = (math.log((float(max_timescale) / float(min_timescale))) / (tf.to_float(num_timescales) - 1))
        inv_timescales = (min_timescale * tf.exp((tf.to_float(tf.range(num_timescales)) * (- log_timescale_increment))))
        scaled_time = (tf.expand_dims(position, 1) * tf.expand_dims(inv_timescales, 0))
        signal = tf.concat([tf.sin(scaled_time), tf.cos(scaled_time)], axis=1)
        signal = tf.pad(signal, [[0, 0], [0, tf.mod(channels, 2)]])
        signal = tf.reshape(signal, [1, length, channels])
        return (x + signal)
