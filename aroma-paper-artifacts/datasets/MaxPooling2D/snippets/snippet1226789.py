from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import functools
import six
from tensorflow.contrib.framework.python.ops import add_arg_scope
from tensorflow.contrib.framework.python.ops import variables
from tensorflow.contrib.layers.python.layers import initializers
from tensorflow.contrib.layers.python.layers import utils
from tensorflow.python.eager import context
from tensorflow.python.framework import constant_op
from tensorflow.python.framework import dtypes
from tensorflow.python.framework import function
from tensorflow.python.framework import ops
from tensorflow.python.framework import sparse_tensor
from tensorflow.python.framework import tensor_shape
from tensorflow.python.layers import base
from tensorflow.python.layers import convolutional as convolutional_layers
from tensorflow.python.layers import core as core_layers
from tensorflow.python.layers import normalization as normalization_layers
from tensorflow.python.layers import pooling as pooling_layers
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import check_ops
from tensorflow.python.ops import init_ops
from tensorflow.python.ops import linalg_ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import nn
from tensorflow.python.ops import sparse_ops
from tensorflow.python.ops import standard_ops
from tensorflow.python.ops import variable_scope
from tensorflow.python.ops import variables as tf_variables
from tensorflow.python.training import moving_averages


@add_arg_scope
def max_pool2d(inputs, kernel_size, stride=2, padding='VALID', data_format=DATA_FORMAT_NHWC, outputs_collections=None, scope=None):
    "Adds a 2D Max Pooling op.\n\n  It is assumed that the pooling is done per image but not in batch or channels.\n\n  Args:\n    inputs: A 4-D tensor of shape `[batch_size, height, width, channels]` if\n      `data_format` is `NHWC`, and `[batch_size, channels, height, width]` if\n      `data_format` is `NCHW`.\n    kernel_size: A list of length 2: [kernel_height, kernel_width] of the\n      pooling kernel over which the op is computed. Can be an int if both\n      values are the same.\n    stride: A list of length 2: [stride_height, stride_width].\n      Can be an int if both strides are the same. Note that presently\n      both strides must have the same value.\n    padding: The padding method, either 'VALID' or 'SAME'.\n    data_format: A string. `NHWC` (default) and `NCHW` are supported.\n    outputs_collections: The collections to which the outputs are added.\n    scope: Optional scope for name_scope.\n\n  Returns:\n    A `Tensor` representing the results of the pooling operation.\n\n  Raises:\n    ValueError: If `data_format` is neither `NHWC` nor `NCHW`.\n    ValueError: If 'kernel_size' is not a 2-D list\n  "
    if (data_format not in (DATA_FORMAT_NCHW, DATA_FORMAT_NHWC)):
        raise ValueError('data_format has to be either NCHW or NHWC.')
    with ops.name_scope(scope, 'MaxPool2D', [inputs]) as sc:
        inputs = ops.convert_to_tensor(inputs)
        df = ('channels_first' if (data_format and data_format.startswith('NC')) else 'channels_last')
        layer = pooling_layers.MaxPooling2D(pool_size=kernel_size, strides=stride, padding=padding, data_format=df, _scope=sc)
        outputs = layer.apply(inputs)
        return utils.collect_named_outputs(outputs_collections, sc, outputs)
