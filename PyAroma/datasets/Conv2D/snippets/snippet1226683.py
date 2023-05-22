from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
import pdb
from tensorflow.python.framework import ops
from tensorflow.python.framework import tensor_shape
from tensorflow.python.layers import base
from tensorflow.python.layers import utils
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import init_ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import nn
from tensorflow.python.ops import standard_ops
from tensorflow.python.ops import control_flow_ops
import pdb


def __init__(self, filters, kernel_size, strides=(1, 1), padding='valid', data_format='channels_last', dilation_rate=(1, 1), depth_multiplier=1, activation=None, use_bias=True, depthwise_initializer='global_uniform', pointwise_initializer='global_uniform', depthwise_regularizer=None, pointwise_regularizer=None, bias_initializer=init_ops.zeros_initializer(), bias_regularizer=None, activity_regularizer=None, trainable=True, name=None, task_id=1, **kwargs):
    super(MaskedSeparableConv2D, self).__init__(rank=2, filters=filters, kernel_size=kernel_size, strides=strides, padding=padding, data_format=data_format, dilation_rate=dilation_rate, activation=activation, use_bias=use_bias, bias_initializer=bias_initializer, bias_regularizer=bias_regularizer, activity_regularizer=activity_regularizer, trainable=trainable, name=name, task_id=task_id, **kwargs)
    self.depth_multiplier = depth_multiplier
    self.depthwise_initializer = depthwise_initializer
    self.pointwise_initializer = pointwise_initializer
    self.depthwise_regularizer = depthwise_regularizer
    self.pointwise_regularizer = pointwise_regularizer
