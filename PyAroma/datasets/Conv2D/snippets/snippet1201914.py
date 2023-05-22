import keras.backend as K
from keras.layers import Conv2DTranspose as Transpose
from keras.layers import UpSampling2D
from keras.layers import Conv2D
from keras.layers import BatchNormalization
from keras.layers import Activation
from keras.layers import Add


def layer(x):
    x = Conv2D(filters, kernel_size, padding='same', name=conv_name, use_bias=(not use_batchnorm))(x)
    if use_batchnorm:
        x = BatchNormalization(name=bn_name)(x)
    x = Activation('relu', name=relu_name)(x)
    return x