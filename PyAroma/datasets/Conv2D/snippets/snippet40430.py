import numpy as np
from keras.layers import MaxPool2D
from keras.layers import AveragePooling2D
from keras.layers import Concatenate
from keras.layers import Permute
from keras.layers import Reshape
from keras.backend import int_shape
from ..common import Conv2DBlock
from ..common import ResizeImage


def layer(input_tensor):
    pool_size = [int(np.round((feature_map_shape[0] / level))), int(np.round((feature_map_shape[1] / level)))]
    strides = pool_size
    x = Pool2D(pool_size, strides=strides, padding=pool_padding)(input_tensor)
    x = Conv2DBlock(conv_filters, kernel_size=conv_kernel_size, padding=conv_padding, use_batchnorm=use_batchnorm, activation=activation, name='level{}'.format(level))(x)
    x = ResizeImage(strides, interpolation=interpolation)(x)
    return x
