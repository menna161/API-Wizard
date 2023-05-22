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


def call(self, inputs):
    if (self.data_format == 'channels_first'):
        if (self.cropping[0][1] == self.cropping[1][1] == 0):
            return inputs[(:, :, self.cropping[0][0]:, self.cropping[1][0]:)]
        elif (self.cropping[0][1] == 0):
            return inputs[(:, :, self.cropping[0][0]:, self.cropping[1][0]:(- self.cropping[1][1]))]
        elif (self.cropping[1][1] == 0):
            return inputs[(:, :, self.cropping[0][0]:(- self.cropping[0][1]), self.cropping[1][0]:)]
        return inputs[(:, :, self.cropping[0][0]:(- self.cropping[0][1]), self.cropping[1][0]:(- self.cropping[1][1]))]
    else:
        if (self.cropping[0][1] == self.cropping[1][1] == 0):
            return inputs[(:, self.cropping[0][0]:, self.cropping[1][0]:, :)]
        elif (self.cropping[0][1] == 0):
            return inputs[(:, self.cropping[0][0]:, self.cropping[1][0]:(- self.cropping[1][1]), :)]
        elif (self.cropping[1][1] == 0):
            return inputs[(:, self.cropping[0][0]:(- self.cropping[0][1]), self.cropping[1][0]:, :)]
        return inputs[(:, self.cropping[0][0]:(- self.cropping[0][1]), self.cropping[1][0]:(- self.cropping[1][1]), :)]
