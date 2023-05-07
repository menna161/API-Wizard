import string
import numpy as np
import tensorflow as tf
from tensorflow.contrib.layers.python.layers import layers
from tensorflow.python.layers import base as base_layer
from tensorflow.python.framework import tensor_shape
from tensorflow.python.framework import dtypes
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import init_ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import nn_ops
from tensorflow.python.ops import rnn_cell_impl
from tensorflow.contrib.rnn import LayerRNNCell, LayerNormBasicLSTMCell, BasicRNNCell
from tensorflow.python.ops import variable_scope as vs
from tensorflow.python.platform import tf_logging as logging
from tensorflow.python.util import nest
from nabu.neuralnetworks.components import ops
from nabu.neuralnetworks.components import rnn_cell_impl as rnn_cell_impl_extended
from ops import capsule_initializer
from ntm_ops import create_linear_initializer
import collections


def addressing(self, k, beta, g, s, gamma, prev_M, prev_w):
    num_head = prev_w.get_shape()[1]
    k = tf.expand_dims(k, axis=(- 1))
    k_norm = tf.norm(k, axis=2, keepdims=True)
    k_normalized = (k / (k_norm + 1e-12))
    prev_M = tf.tile(tf.expand_dims(prev_M, 1), [1, num_head, 1, 1])
    prev_M_norm = tf.norm(prev_M, axis=(- 1), keepdims=True)
    prev_M_normalized = (prev_M / (prev_M_norm + 1e-12))
    K = tf.squeeze(tf.matmul(prev_M_normalized, k_normalized), (- 1))
    K_amplified = tf.exp((tf.expand_dims(beta, axis=2) * K))
    w_c = tf.nn.softmax(K_amplified, axis=2)
    if (self.addressing_mode == 'content'):
        return w_c
    g = tf.expand_dims(g, axis=2)
    w_g = ((g * w_c) + ((1 - g) * prev_w))
    if (self.addressing_mode == 'content_gated'):
        return w_g
    shift_range = (self.shift_win_size / 2)
    s = tf.concat([s[(:, :, :(shift_range + 1))], tf.zeros(s.get_shape()[0:2].concatenate(tf.TensorShape([(self.memory_size - self.shift_win_size)]))), s[(:, :, (shift_range + 1):)]], axis=(- 1))
    t = tf.concat([tf.reverse(s, axis=[(- 1)]), tf.reverse(s, axis=[(- 1)])], axis=(- 1))
    s_matrix = tf.stack([t[(:, :, ((self.memory_size - i) - 1):(((self.memory_size * 2) - i) - 1))] for i in range(self.memory_size)], axis=(- 1))
    w_ = tf.reduce_sum((tf.expand_dims(w_g, axis=2) * s_matrix), axis=(- 1))
    w_sharpen = tf.pow(w_, tf.expand_dims(gamma, axis=(- 1)))
    w = (w_sharpen / tf.reduce_sum(w_sharpen, axis=(- 1), keep_dims=True))
    return w
