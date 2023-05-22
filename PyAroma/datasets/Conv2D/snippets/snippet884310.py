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


def resblock_body(x, num_filters, num_blocks, all_narrow=True):
    'A series of resblocks starting with a downsampling Convolution2D'
    preconv1 = ZeroPadding2D(((1, 0), (1, 0)))(x)
    preconv1 = DarknetConv2D_BN_Mish(num_filters, (3, 3), strides=(2, 2))(preconv1)
    shortconv = DarknetConv2D_BN_Mish(((num_filters // 2) if all_narrow else num_filters), (1, 1))(preconv1)
    mainconv = DarknetConv2D_BN_Mish(((num_filters // 2) if all_narrow else num_filters), (1, 1))(preconv1)
    for i in range(num_blocks):
        y = compose(DarknetConv2D_BN_Mish((num_filters // 2), (1, 1)), DarknetConv2D_BN_Mish(((num_filters // 2) if all_narrow else num_filters), (3, 3)))(mainconv)
        mainconv = Add()([mainconv, y])
    postconv = DarknetConv2D_BN_Mish(((num_filters // 2) if all_narrow else num_filters), (1, 1))(mainconv)
    route = Concatenate()([postconv, shortconv])
    return DarknetConv2D_BN_Mish(num_filters, (1, 1))(route)
