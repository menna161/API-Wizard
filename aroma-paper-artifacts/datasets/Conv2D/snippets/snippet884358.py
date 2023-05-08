import functools
from functools import partial
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.normalization import BatchNormalization
from keras.models import Model
from keras.regularizers import l2
from ..utils import compose


@functools.wraps(Conv2D)
def DarknetConv2D(*args, **kwargs):
    'Wrapper to set Darknet weight regularizer for Convolution2D.'
    darknet_conv_kwargs = {'kernel_regularizer': l2(0.0005)}
    darknet_conv_kwargs.update(kwargs)
    return _DarknetConv2D(*args, **darknet_conv_kwargs)
