from functools import wraps
import numpy as np
import tensorflow as tf
from keras import backend as K
from keras.layers import Conv2D, Add, ZeroPadding2D, UpSampling2D, Concatenate, MaxPooling2D
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.normalization import BatchNormalization
from keras.models import Model
from keras.regularizers import l2
from yolo3.utils import compose


def make_last_layers(x, num_filters, out_filters):
    '6 Conv2D_BN_Leaky layers followed by a Conv2D_linear layer'
    x = compose(DarknetConv2D_BN_Leaky(num_filters, (1, 1)), DarknetConv2D_BN_Leaky((num_filters * 2), (3, 3)), DarknetConv2D_BN_Leaky(num_filters, (1, 1)), DarknetConv2D_BN_Leaky((num_filters * 2), (3, 3)), DarknetConv2D_BN_Leaky(num_filters, (1, 1)))(x)
    y = compose(DarknetConv2D_BN_Leaky((num_filters * 2), (3, 3)), DarknetConv2D(out_filters, (1, 1)))(x)
    return (x, y)
