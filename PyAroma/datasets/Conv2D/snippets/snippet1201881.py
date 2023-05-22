from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import warnings
from keras.models import Model
from keras import layers
from keras.layers import Activation
from keras.layers import Dense
from keras.layers import Input
from keras.layers import BatchNormalization
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import AveragePooling2D
from keras.layers import GlobalAveragePooling2D
from keras.layers import GlobalMaxPooling2D
from keras.engine.topology import get_source_inputs
from keras.utils.data_utils import get_file
from keras import backend as K
from keras.applications import imagenet_utils
import keras
from distutils.version import StrictVersion
from keras.applications.imagenet_utils import _obtain_input_shape
from keras_applications.imagenet_utils import _obtain_input_shape


def conv2d_bn(x, filters, num_row, num_col, padding='same', strides=(1, 1), name=None):
    "Utility function to apply conv + BN.\n    # Arguments\n        x: input tensor.\n        filters: filters in `Conv2D`.\n        num_row: height of the convolution kernel.\n        num_col: width of the convolution kernel.\n        padding: padding mode in `Conv2D`.\n        strides: strides in `Conv2D`.\n        name: name of the ops; will become `name + '_conv'`\n            for the convolution and `name + '_bn'` for the\n            batch norm layer.\n    # Returns\n        Output tensor after applying `Conv2D` and `BatchNormalization`.\n    "
    if (name is not None):
        bn_name = (name + '_bn')
        conv_name = (name + '_conv')
    else:
        bn_name = None
        conv_name = None
    if (K.image_data_format() == 'channels_first'):
        bn_axis = 1
    else:
        bn_axis = 3
    x = Conv2D(filters, (num_row, num_col), strides=strides, padding=padding, use_bias=False, name=conv_name)(x)
    x = BatchNormalization(axis=bn_axis, scale=False, name=bn_name)(x)
    x = Activation('relu', name=name)(x)
    return x
