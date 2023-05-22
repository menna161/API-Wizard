from keras.layers import Conv2D
from keras.layers import Add
from keras.layers import Activation
from keras.layers import BatchNormalization
import keras
from distutils.version import StrictVersion
from .layers import UpSampling2D
from keras.layers import UpSampling2D


def Conv(n_filters, kernel_size, activation='relu', use_batchnorm=False, **kwargs):
    'Extension of Conv2aaD layer with batchnorm'

    def layer(input_tensor):
        x = Conv2D(n_filters, kernel_size, use_bias=(not use_batchnorm), **kwargs)(input_tensor)
        if use_batchnorm:
            x = BatchNormalization()(x)
        x = Activation(activation)(x)
        return x
    return layer
