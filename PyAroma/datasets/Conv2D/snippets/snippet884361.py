import functools
from functools import partial
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.normalization import BatchNormalization
from keras.models import Model
from keras.regularizers import l2
from ..utils import compose


def bottleneck_x2_block(outer_filters, bottleneck_filters):
    'Bottleneck block of 3x3, 1x1, 3x3, 1x1, 3x3 convolutions.'
    return compose(bottleneck_block(outer_filters, bottleneck_filters), DarknetConv2D_BN_Leaky(bottleneck_filters, (1, 1)), DarknetConv2D_BN_Leaky(outer_filters, (3, 3)))
