from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import warnings
from keras.models import Model
from keras.layers import Activation
from keras.layers import AveragePooling2D
from keras.layers import BatchNormalization
from keras.layers import Conv2D
from keras.layers import Concatenate
from keras.layers import Dense
from keras.layers import GlobalAveragePooling2D
from keras.layers import GlobalMaxPooling2D
from keras.layers import Input
from keras.layers import Lambda
from keras.layers import MaxPooling2D
from keras.utils.data_utils import get_file
from keras.engine.topology import get_source_inputs
from keras.applications import imagenet_utils
from keras import backend as K
import keras
from distutils.version import StrictVersion
from keras.applications.imagenet_utils import _obtain_input_shape
from keras_applications.imagenet_utils import _obtain_input_shape


def conv2d_bn(x, filters, kernel_size, strides=1, padding='same', activation='relu', use_bias=False, name=None):
    "Utility function to apply conv + BN.\n    # Arguments\n        x: input tensor.\n        filters: filters in `Conv2D`.\n        kernel_size: kernel size as in `Conv2D`.\n        strides: strides in `Conv2D`.\n        padding: padding mode in `Conv2D`.\n        activation: activation in `Conv2D`.\n        use_bias: whether to use a bias in `Conv2D`.\n        name: name of the ops; will become `name + '_ac'` for the activation\n            and `name + '_bn'` for the batch norm layer.\n    # Returns\n        Output tensor after applying `Conv2D` and `BatchNormalization`.\n    "
    x = Conv2D(filters, kernel_size, strides=strides, padding=padding, use_bias=use_bias, name=name)(x)
    if (not use_bias):
        bn_axis = (1 if (K.image_data_format() == 'channels_first') else 3)
        bn_name = (None if (name is None) else (name + '_bn'))
        x = BatchNormalization(axis=bn_axis, scale=False, name=bn_name)(x)
    if (activation is not None):
        ac_name = (None if (name is None) else (name + '_ac'))
        x = Activation(activation, name=ac_name)(x)
    return x
