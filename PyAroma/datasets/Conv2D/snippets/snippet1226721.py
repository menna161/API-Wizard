from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from tensorflow.python.eager import context
from tensorflow.python.framework import tensor_shape
from tensorflow.python.keras import activations
from tensorflow.python.keras import backend
from tensorflow.python.keras import constraints
from tensorflow.python.keras import initializers
from tensorflow.python.keras import regularizers
from tensorflow.python.keras.engine.base_layer import InputSpec
from tensorflow.python.keras.engine.base_layer import Layer
from tensorflow.python.keras.layers.pooling import AveragePooling1D
from tensorflow.python.keras.layers.pooling import AveragePooling2D
from tensorflow.python.keras.layers.pooling import AveragePooling3D
from tensorflow.python.keras.layers.pooling import MaxPooling1D
from tensorflow.python.keras.layers.pooling import MaxPooling2D
from tensorflow.python.keras.layers.pooling import MaxPooling3D
from tensorflow.python.keras.utils import conv_utils
from tensorflow.python.keras.utils import tf_utils
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import nn
from tensorflow.python.ops import nn_ops
from tensorflow.python.util.tf_export import tf_export


def __init__(self, filters, kernel_size, strides=(1, 1), padding='valid', data_format=None, dilation_rate=(1, 1), depth_multiplier=1, activation=None, use_bias=True, depthwise_initializer='glorot_uniform', pointwise_initializer='glorot_uniform', bias_initializer='zeros', depthwise_regularizer=None, pointwise_regularizer=None, bias_regularizer=None, activity_regularizer=None, depthwise_constraint=None, pointwise_constraint=None, bias_constraint=None, **kwargs):
    super(SeparableConv2D, self).__init__(rank=2, filters=filters, kernel_size=kernel_size, strides=strides, padding=padding, data_format=data_format, dilation_rate=dilation_rate, depth_multiplier=depth_multiplier, activation=activations.get(activation), use_bias=use_bias, depthwise_initializer=initializers.get(depthwise_initializer), pointwise_initializer=initializers.get(pointwise_initializer), bias_initializer=initializers.get(bias_initializer), depthwise_regularizer=regularizers.get(depthwise_regularizer), pointwise_regularizer=regularizers.get(pointwise_regularizer), bias_regularizer=regularizers.get(bias_regularizer), activity_regularizer=regularizers.get(activity_regularizer), depthwise_constraint=constraints.get(depthwise_constraint), pointwise_constraint=constraints.get(pointwise_constraint), bias_constraint=constraints.get(bias_constraint), **kwargs)
