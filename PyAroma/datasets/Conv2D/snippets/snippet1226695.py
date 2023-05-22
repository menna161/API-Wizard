from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import six
from tensorflow.contrib.framework.python.ops import add_arg_scope
from tensorflow.contrib.framework.python.ops import variables
from tensorflow.contrib.layers.python.layers import initializers
from tensorflow.contrib.layers.python.layers import utils
import sys, os
from core_layers import MaskedConv2D, MaskedSeparableConv2D, MaskedFullyConnected
from tensorflow.python.framework import ops
from tensorflow.python.ops import init_ops
from tensorflow.python.ops import nn
from tensorflow.python.ops import variable_scope
from tensorflow.python.ops import variables as tf_variables
import tensorflow as tf
from tensorflow.python.layers import core as core_layers


@add_arg_scope
def masked_separable_convolution2d(inputs, num_outputs, kernel_size, depth_multiplier, stride=1, padding='SAME', data_format=None, rate=1, activation_fn=nn.relu, normalizer_fn=None, normalizer_params=None, weights_initializer=initializers.xavier_initializer(), weights_regularizer=None, biases_initializer=init_ops.zeros_initializer(), biases_regularizer=None, reuse=None, variables_collections=None, outputs_collections=None, trainable=True, scope=None, task_id=1):
    if (data_format not in [None, 'NHWC', 'NCHW']):
        raise ValueError(('Invalid data_format: %r' % (data_format,)))
    layer_variable_getter = _build_variable_getter({'bias': 'biases', 'depthwise_kernel': 'depthwise_weights', 'pointwise_kernel': 'pointwise_weights'})
    with variable_scope.variable_scope(scope, 'SeparableConv2d', [inputs], reuse=reuse, custom_getter=layer_variable_getter) as sc:
        inputs = ops.convert_to_tensor(inputs)
        if ((data_format is None) or (data_format == 'NHWC')):
            df = 'channels_last'
        elif (data_format == 'NCHW'):
            df = 'channels_first'
        else:
            raise ValueError('Unsupported data format', data_format)
        if (num_outputs is not None):
            layer = MaskedSeparableConv2D(filters=num_outputs, kernel_size=kernel_size, strides=stride, padding=padding, data_format=df, dilation_rate=utils.two_element_tuple(rate), activation=None, depth_multiplier=depth_multiplier, use_bias=((not normalizer_fn) and biases_initializer), depthwise_initializer=weights_initializer, pointwise_initializer=weights_initializer, depthwise_regularizer=weights_regularizer, pointwise_regularizer=weights_regularizer, bias_initializer=biases_initializer, bias_regularizer=biases_regularizer, activity_regularizer=None, trainable=trainable, name=sc.name, dtype=inputs.dtype.base_dtype, task_id=task_id, _scope=sc, _reuse=reuse)
            outputs = layer.apply(inputs)
            _add_variable_to_collections(layer.depthwise_kernel, variables_collections, 'weights')
            _add_variable_to_collections(layer.pointwise_kernel, variables_collections, 'weights')
            if layer.use_bias:
                _add_variable_to_collections(layer.bias, variables_collections, 'biases')
            if (normalizer_fn is not None):
                normalizer_params = (normalizer_params or {})
                with tf.variable_scope('task_{}'.format(task_id)):
                    outputs = normalizer_fn(outputs, **normalizer_params)
        else:
            raise ValueError('Num Outputs is None, Need to apply depthwise conv2d')
        if (activation_fn is not None):
            outputs = activation_fn(outputs)
        return utils.collect_named_outputs(outputs_collections, sc.original_name_scope, outputs)
