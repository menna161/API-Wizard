from keras.layers import Conv2D
from keras.layers import Add
from keras.layers import Activation
from keras.layers import BatchNormalization
import keras
from distutils.version import StrictVersion
from .layers import UpSampling2D
from keras.layers import UpSampling2D


def layer(c, m=None):
    x = Conv2D(pyramid_filters, (1, 1))(c)
    if (m is not None):
        up = UpSampling2D((upsample_rate, upsample_rate))(m)
        x = Add()([x, up])
    p = Conv(segmentation_filters, (3, 3), padding='same', use_batchnorm=use_batchnorm)(x)
    p = Conv(segmentation_filters, (3, 3), padding='same', use_batchnorm=use_batchnorm)(p)
    m = x
    return (m, p)
