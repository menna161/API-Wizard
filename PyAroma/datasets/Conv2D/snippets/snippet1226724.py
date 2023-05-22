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


def build(self, input_shape):
    if (len(input_shape) < 4):
        raise ValueError('Inputs to `DepthwiseConv2D` should have rank 4. Received input shape:', str(input_shape))
    if (self.data_format == 'channels_first'):
        channel_axis = 1
    else:
        channel_axis = 3
    if (input_shape[channel_axis] is None):
        raise ValueError('The channel dimension of the inputs to `DepthwiseConv2D` should be defined. Found `None`.')
    input_dim = int(input_shape[channel_axis])
    depthwise_kernel_shape = (self.kernel_size[0], self.kernel_size[1], input_dim, self.depth_multiplier)
    self.depthwise_kernel = self.add_weight(shape=depthwise_kernel_shape, initializer=self.depthwise_initializer, name='depthwise_kernel', regularizer=self.depthwise_regularizer, constraint=self.depthwise_constraint)
    if self.use_bias:
        self.bias = self.add_weight(shape=((input_dim * self.depth_multiplier),), initializer=self.bias_initializer, name='bias', regularizer=self.bias_regularizer, constraint=self.bias_constraint)
    else:
        self.bias = None
    self.input_spec = InputSpec(ndim=4, axes={channel_axis: input_dim})
    self.built = True
