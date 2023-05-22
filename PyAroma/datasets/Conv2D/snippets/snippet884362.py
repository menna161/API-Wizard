import functools
from functools import partial
from keras.layers import Conv2D, MaxPooling2D
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.normalization import BatchNormalization
from keras.models import Model
from keras.regularizers import l2
from ..utils import compose


def darknet_body():
    'Generate first 18 conv layers of Darknet-19.'
    return compose(DarknetConv2D_BN_Leaky(32, (3, 3)), MaxPooling2D(), DarknetConv2D_BN_Leaky(64, (3, 3)), MaxPooling2D(), bottleneck_block(128, 64), MaxPooling2D(), bottleneck_block(256, 128), MaxPooling2D(), bottleneck_x2_block(512, 256), MaxPooling2D(), bottleneck_x2_block(1024, 512))
