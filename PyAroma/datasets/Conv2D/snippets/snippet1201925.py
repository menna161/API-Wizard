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
    (h, w, c) = int_shape(input_tensor)[1:]
    H = (h * factor)
    W = (w * factor)
    x = Conv2DBlock((c * (factor ** 2)), (1, 1), padding='same', name='duc_{}'.format(factor))(input_tensor)
    x = Permute((3, 1, 2))(x)
    x = Reshape((c, factor, factor, h, w))(x)
    x = Permute((1, 4, 2, 5, 3))(x)
    x = Reshape((c, H, W))(x)
    x = Permute((2, 3, 1))(x)
    return x
