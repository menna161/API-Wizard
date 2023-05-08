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
def masked_convolution(inputs, num_outputs, kernel_size, stride=1, padding='SAME', data_format=None, rate=1, activation_fn=nn.relu, normalizer_fn=None, normalizer_params=None, weights_initializer=initializers.xavier_initializer(), weights_regularizer=None, biases_initializer=init_ops.zeros_initializer(), biases_regularizer=None, reuse=None, variables_collections=None, outputs_collections=None, trainable=True, scope=None, task_id=1):
    'Adds an 2D convolution followed by an optional batch_norm layer.\n  The layer creates a mask variable on top of the weight variable. The input to\n  the convolution operation is the elementwise multiplication of the mask\n  variable and the weigh\n\n  It is required that 1 <= N <= 3.\n\n  `convolution` creates a variable called `weights`, representing the\n  convolutional kernel, that is convolved (actually cross-correlated) with the\n  `inputs` to produce a `Tensor` of activations. If a `normalizer_fn` is\n  provided (such as `batch_norm`), it is then applied. Otherwise, if\n  `normalizer_fn` is None and a `biases_initializer` is provided then a `biases`\n  variable would be created and added the activations. Finally, if\n  `activation_fn` is not `None`, it is applied to the activations as well.\n\n  Performs atrous convolution with input stride/dilation rate equal to `rate`\n  if a value > 1 for any dimension of `rate` is specified.  In this case\n  `stride` values != 1 are not supported.\n\n  Args:\n    inputs: A Tensor of rank N+2 of shape\n      `[batch_size] + input_spatial_shape + [in_channels]` if data_format does\n      not start with "NC" (default), or\n      `[batch_size, in_channels] + input_spatial_shape` if data_format starts\n      with "NC".\n    num_outputs: Integer, the number of output filters.\n    kernel_size: A sequence of N positive integers specifying the spatial\n      dimensions of of the filters.  Can be a single integer to specify the same\n      value for all spatial dimensions.\n    stride: A sequence of N positive integers specifying the stride at which to\n      compute output.  Can be a single integer to specify the same value for all\n      spatial dimensions.  Specifying any `stride` value != 1 is incompatible\n      with specifying any `rate` value != 1.\n    padding: One of `"VALID"` or `"SAME"`.\n    data_format: A string or None.  Specifies whether the channel dimension of\n      the `input` and output is the last dimension (default, or if `data_format`\n      does not start with "NC"), or the second dimension (if `data_format`\n      starts with "NC").  For N=1, the valid values are "NWC" (default) and\n      "NCW".  For N=2, the valid values are "NHWC" (default) and "NCHW".\n      For N=3, the valid values are "NDHWC" (default) and "NCDHW".\n    rate: A sequence of N positive integers specifying the dilation rate to use\n      for atrous convolution.  Can be a single integer to specify the same\n      value for all spatial dimensions.  Specifying any `rate` value != 1 is\n      incompatible with specifying any `stride` value != 1.\n    activation_fn: Activation function. The default value is a ReLU function.\n      Explicitly set it to None to skip it and maintain a linear activation.\n    normalizer_fn: Normalization function to use instead of `biases`. If\n      `normalizer_fn` is provided then `biases_initializer` and\n      `biases_regularizer` are ignored and `biases` are not created nor added.\n      default set to None for no normalizer function\n    normalizer_params: Normalization function parameters.\n    weights_initializer: An initializer for the weights.\n    weights_regularizer: Optional regularizer for the weights.\n    biases_initializer: An initializer for the biases. If None skip biases.\n    biases_regularizer: Optional regularizer for the biases.\n    reuse: Whether or not the layer and its variables should be reused. To be\n      able to reuse the layer scope must be given.\n    variables_collections: Optional list of collections for all the variables or\n      a dictionary containing a different list of collection per variable.\n    outputs_collections: Collection to add the outputs.\n    trainable: If `True` also add variables to the graph collection\n      `GraphKeys.TRAINABLE_VARIABLES` (see tf.Variable).\n    scope: Optional scope for `variable_scope`.\n\n  Returns:\n    A tensor representing the output of the operation.\n\n  Raises:\n    ValueError: If `data_format` is invalid.\n    ValueError: Both \'rate\' and `stride` are not uniformly 1.\n  '
    if (data_format not in [None, 'NWC', 'NCW', 'NHWC', 'NCHW', 'NDHWC', 'NCDHW']):
        raise ValueError(('Invalid data_format: %r' % (data_format,)))
    layer_variable_getter = _build_variable_getter({'bias': 'biases', 'kernel': 'weights'})
    with variable_scope.variable_scope(scope, 'Conv', [inputs], reuse=reuse, custom_getter=layer_variable_getter) as sc:
        inputs = ops.convert_to_tensor(inputs)
        input_rank = inputs.get_shape().ndims
        if (input_rank == 3):
            raise ValueError('Sparse Convolution not supported for input with rank', input_rank)
        elif (input_rank == 4):
            layer_class = MaskedConv2D
        elif (input_rank == 5):
            raise ValueError('Sparse Convolution not supported for input with rank', input_rank)
        else:
            raise ValueError('Sparse Convolution not supported for input with rank', input_rank)
        if ((data_format is None) or (data_format == 'NHWC')):
            df = 'channels_last'
        elif (data_format == 'NCHW'):
            df = 'channels_first'
        else:
            raise ValueError('Unsupported data format', data_format)
        layer = layer_class(filters=num_outputs, kernel_size=kernel_size, strides=stride, padding=padding, data_format=df, dilation_rate=rate, activation=None, use_bias=((not normalizer_fn) and biases_initializer), kernel_initializer=weights_initializer, bias_initializer=biases_initializer, kernel_regularizer=weights_regularizer, bias_regularizer=biases_regularizer, activity_regularizer=None, trainable=trainable, name=sc.name, dtype=inputs.dtype.base_dtype, task_id=task_id, _scope=sc, _reuse=reuse)
        outputs = layer.apply(inputs)
        _add_variable_to_collections(layer.kernel, variables_collections, 'weights')
        if layer.use_bias:
            _add_variable_to_collections(layer.bias, variables_collections, 'biases')
        if (normalizer_fn is not None):
            normalizer_params = (normalizer_params or {})
            with tf.variable_scope('task_{}'.format(task_id)):
                outputs = normalizer_fn(outputs, **normalizer_params)
        if (activation_fn is not None):
            outputs = activation_fn(outputs)
        return utils.collect_named_outputs(outputs_collections, sc.original_name_scope, outputs)
