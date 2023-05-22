from __future__ import print_function
from collections import defaultdict
import contextlib
import numpy as np
import tensorflow as tf
from tensorflow.python.layers import convolutional as conv_layers
from tensorflow.python.layers import core as core_layers
from tensorflow.python.layers import pooling as pooling_layers
from tensorflow.python.training import moving_averages


def conv(self, num_out_channels, k_height, k_width, d_height=1, d_width=1, mode='SAME', input_layer=None, num_channels_in=None, use_batch_norm=None, stddev=None, activation='relu', bias=0.0, kernel_initializer=None):
    'Construct a conv2d layer on top of cnn.'
    if (input_layer is None):
        input_layer = self.top_layer
    if (num_channels_in is None):
        num_channels_in = self.top_size
    if ((stddev is not None) and (kernel_initializer is None)):
        kernel_initializer = tf.truncated_normal_initializer(stddev=stddev)
    name = ('conv' + str(self.counts['conv']))
    self.counts['conv'] += 1
    with tf.variable_scope(name):
        strides = [1, d_height, d_width, 1]
        if (self.data_format == 'NCHW'):
            strides = [strides[0], strides[3], strides[1], strides[2]]
        if (mode != 'SAME_RESNET'):
            conv = self._conv2d_impl(input_layer, num_channels_in, num_out_channels, kernel_size=[k_height, k_width], strides=[d_height, d_width], padding=mode, kernel_initializer=kernel_initializer)
        elif ((d_height == 1) and (d_width == 1)):
            conv = self._conv2d_impl(input_layer, num_channels_in, num_out_channels, kernel_size=[k_height, k_width], strides=[d_height, d_width], padding='SAME', kernel_initializer=kernel_initializer)
        else:
            rate = 1
            kernel_height_effective = (k_height + ((k_height - 1) * (rate - 1)))
            pad_h_beg = ((kernel_height_effective - 1) // 2)
            pad_h_end = ((kernel_height_effective - 1) - pad_h_beg)
            kernel_width_effective = (k_width + ((k_width - 1) * (rate - 1)))
            pad_w_beg = ((kernel_width_effective - 1) // 2)
            pad_w_end = ((kernel_width_effective - 1) - pad_w_beg)
            padding = [[0, 0], [pad_h_beg, pad_h_end], [pad_w_beg, pad_w_end], [0, 0]]
            if (self.data_format == 'NCHW'):
                padding = [padding[0], padding[3], padding[1], padding[2]]
            input_layer = tf.pad(input_layer, padding)
            conv = self._conv2d_impl(input_layer, num_channels_in, num_out_channels, kernel_size=[k_height, k_width], strides=[d_height, d_width], padding='VALID', kernel_initializer=kernel_initializer)
        if (use_batch_norm is None):
            use_batch_norm = self.use_batch_norm
        if (not use_batch_norm):
            if (bias is not None):
                biases = self.get_variable('biases', [num_out_channels], self.variable_dtype, self.dtype, initializer=tf.constant_initializer(bias))
                biased = tf.reshape(tf.nn.bias_add(conv, biases, data_format=self.data_format), conv.get_shape())
            else:
                biased = conv
        else:
            self.top_layer = conv
            self.top_size = num_out_channels
            biased = self.batch_norm(**self.batch_norm_config)
        if (activation == 'relu'):
            conv1 = tf.nn.relu(biased)
        elif ((activation == 'linear') or (activation is None)):
            conv1 = biased
        elif (activation == 'tanh'):
            conv1 = tf.nn.tanh(biased)
        else:
            raise KeyError(("Invalid activation type '%s'" % activation))
        self.top_layer = conv1
        self.top_size = num_out_channels
        return conv1
