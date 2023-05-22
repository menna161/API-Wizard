from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
import tensorflow.contrib.layers as layers


def __call__(self, inputs, hidden, cell, global_memory, eidetic_cell):
    with tf.variable_scope(self._layer_name):
        new_hidden = self._conv(hidden, (4 * self._output_channels), self._kernel_shape)
        if self._layer_norm:
            new_hidden = self._norm(new_hidden, 'hidden')
        (i_h, g_h, r_h, o_h) = tf.split(value=new_hidden, num_or_size_splits=4, axis=(- 1))
        new_inputs = self._conv(inputs, (7 * self._output_channels), self._kernel_shape)
        if self._layer_norm:
            new_inputs = self._norm(new_inputs, 'inputs')
            (i_x, g_x, r_x, o_x, temp_i_x, temp_g_x, temp_f_x) = tf.split(value=new_inputs, num_or_size_splits=7, axis=(- 1))
        i_t = tf.sigmoid((i_x + i_h))
        r_t = tf.sigmoid((r_x + r_h))
        g_t = tf.tanh((g_x + g_h))
        new_cell = (cell + self._attn(r_t, eidetic_cell, eidetic_cell))
        new_cell = (self._norm(new_cell, 'self_attn') + (i_t * g_t))
        new_global_memory = self._conv(global_memory, (4 * self._output_channels), self._kernel_shape)
        if self._layer_norm:
            new_global_memory = self._norm(new_global_memory, 'global_memory')
            (i_m, f_m, g_m, m_m) = tf.split(value=new_global_memory, num_or_size_splits=4, axis=(- 1))
        temp_i_t = tf.sigmoid((temp_i_x + i_m))
        temp_f_t = tf.sigmoid(((temp_f_x + f_m) + self._forget_bias))
        temp_g_t = tf.tanh((temp_g_x + g_m))
        new_global_memory = ((temp_f_t * tf.tanh(m_m)) + (temp_i_t * temp_g_t))
        o_c = self._conv(new_cell, self._output_channels, self._kernel_shape)
        o_m = self._conv(new_global_memory, self._output_channels, self._kernel_shape)
        output_gate = tf.tanh((((o_x + o_h) + o_c) + o_m))
        memory = tf.concat([new_cell, new_global_memory], (- 1))
        memory = self._conv(memory, self._output_channels, 1)
        output = (tf.tanh(memory) * tf.sigmoid(output_gate))
    return (output, new_cell, global_memory)
