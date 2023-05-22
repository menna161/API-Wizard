from functools import wraps
import numpy as np
import tensorflow as tf
from keras import backend as K
from keras.engine.base_layer import Layer
from keras.layers import Conv2D, Add, ZeroPadding2D, UpSampling2D, Concatenate, MaxPooling2D
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.normalization import BatchNormalization
from keras.models import Model
from keras.regularizers import l2
from yolo4.utils import compose


@wraps(Conv2D)
def DarknetConv2D(*args, **kwargs):
    'Wrapper to set Darknet parameters for Convolution2D.'
    darknet_conv_kwargs = {'kernel_regularizer': l2(0.0005)}
    darknet_conv_kwargs['padding'] = ('valid' if (kwargs.get('strides') == (2, 2)) else 'same')
    darknet_conv_kwargs.update(kwargs)
    return Conv2D(*args, **darknet_conv_kwargs)
