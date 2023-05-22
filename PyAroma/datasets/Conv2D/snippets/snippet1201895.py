from keras.layers import Conv2D
from keras.layers import Add
from keras.layers import Activation
from keras.layers import BatchNormalization
import keras
from distutils.version import StrictVersion
from .layers import UpSampling2D
from keras.layers import UpSampling2D


def pyramid_block(pyramid_filters=256, segmentation_filters=128, upsample_rate=2, use_batchnorm=False):
    '\n    Pyramid block according to:\n        http://presentations.cocodataset.org/COCO17-Stuff-FAIR.pdf\n\n    This block generate `M` and `P` blocks.\n\n    Args:\n        pyramid_filters: integer, filters in `M` block of top-down FPN branch\n        segmentation_filters: integer, number of filters in segmentation head,\n            basically filters in convolution layers between `M` and `P` blocks\n        upsample_rate: integer, uspsample rate for `M` block of top-down FPN branch\n        use_batchnorm: bool, include batchnorm in convolution blocks\n\n    Returns:\n        Pyramid block function (as Keras layers functional API)\n    '

    def layer(c, m=None):
        x = Conv2D(pyramid_filters, (1, 1))(c)
        if (m is not None):
            up = UpSampling2D((upsample_rate, upsample_rate))(m)
            x = Add()([x, up])
        p = Conv(segmentation_filters, (3, 3), padding='same', use_batchnorm=use_batchnorm)(x)
        p = Conv(segmentation_filters, (3, 3), padding='same', use_batchnorm=use_batchnorm)(p)
        m = x
        return (m, p)
    return layer
