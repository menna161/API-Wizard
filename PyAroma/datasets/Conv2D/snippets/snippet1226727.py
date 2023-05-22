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


def get_config(self):
    config = super(DepthwiseConv2D, self).get_config()
    config.pop('filters')
    config.pop('kernel_initializer')
    config.pop('kernel_regularizer')
    config.pop('kernel_constraint')
    config['depth_multiplier'] = self.depth_multiplier
    config['depthwise_initializer'] = initializers.serialize(self.depthwise_initializer)
    config['depthwise_regularizer'] = regularizers.serialize(self.depthwise_regularizer)
    config['depthwise_constraint'] = constraints.serialize(self.depthwise_constraint)
    return config
