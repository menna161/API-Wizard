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


def __call__(self, inputs, prev_state):
    batch_size = int(inputs.get_shape()[0])
    prev_read_vector = prev_state.read_vector
    combined_inputs = tf.concat([inputs, tf.reshape(prev_read_vector, [batch_size, (self.read_head_num * self.memory_vector_dim)])], axis=1)
    num_parameters_per_head = ((((self.memory_vector_dim + 1) + 1) + self.shift_win_size) + 1)
    num_heads = (self.read_head_num + self.write_head_num)
    num_parameters_erase_per_write_head = self.memory_vector_dim
    total_parameter_num = ((num_parameters_per_head * num_heads) + ((num_parameters_erase_per_write_head * 2) * self.write_head_num))
    with tf.variable_scope('o2p', self.reuse):
        parameters = tf.contrib.layers.fully_connected(combined_inputs, total_parameter_num, activation_fn=None, weights_initializer=self.o2p_initializer)
        parameters = tf.clip_by_value(parameters, (- self.clip_value), self.clip_value)
    head_parameters = parameters[(:, :(num_parameters_per_head * num_heads))]
    head_parameters = tf.reshape(head_parameters, [batch_size, num_heads, num_parameters_per_head])
    erase_parameters = parameters[(:, (num_parameters_per_head * num_heads):((num_parameters_per_head * num_heads) + (num_parameters_erase_per_write_head * self.write_head_num)))]
    erase_parameters = tf.reshape(erase_parameters, [batch_size, self.write_head_num, num_parameters_erase_per_write_head])
    add_parameters = parameters[(:, ((num_parameters_per_head * num_heads) + (num_parameters_erase_per_write_head * self.write_head_num)):)]
    add_parameters = tf.reshape(add_parameters, [batch_size, self.write_head_num, num_parameters_erase_per_write_head])
    prev_w = prev_state.w
    prev_M = prev_state.M
    k = tf.tanh(head_parameters[(:, :, 0:self.memory_vector_dim)])
    beta = tf.nn.softplus(head_parameters[(:, :, self.memory_vector_dim)])
    g = tf.sigmoid(head_parameters[(:, :, (self.memory_vector_dim + 1))])
    s = tf.nn.softmax(head_parameters[(:, :, (self.memory_vector_dim + 2):((self.memory_vector_dim + 2) + self.shift_win_size))], (- 1))
    gamma = (tf.nn.softplus(head_parameters[(:, :, (- 1))]) + 1)
    w = self.addressing(k, beta, g, s, gamma, prev_M, prev_w)
    read_w = tf.expand_dims(w[(:, :self.read_head_num)], (- 1))
    read_vector = tf.reduce_sum((read_w * tf.expand_dims(prev_M, 1)), axis=2)
    M = prev_M
    write_w = tf.expand_dims(w[(:, self.read_head_num:)], (- 1))
    forget_vectors = tf.reduce_prod((1 - tf.matmul(write_w, tf.expand_dims(tf.sigmoid(erase_parameters), 2))), 1)
    add_vectors = tf.reduce_sum(tf.matmul(write_w, tf.expand_dims(tf.tanh(add_parameters), 2)), 1)
    M = ((M * forget_vectors) + add_vectors)
    read_w = tf.squeeze(read_w, (- 1))
    return ((read_vector, read_w), NTMControllerState(read_vector=read_vector, w=w, M=M))
