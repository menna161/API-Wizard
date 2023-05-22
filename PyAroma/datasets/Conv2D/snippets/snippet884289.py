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


def DarknetConv2D_BN_Leaky(*args, **kwargs):
    'Darknet Convolution2D followed by BatchNormalization and LeakyReLU.'
    no_bias_kwargs = {'use_bias': False}
    no_bias_kwargs.update(kwargs)
    return compose(DarknetConv2D(*args, **no_bias_kwargs), BatchNormalization(), LeakyReLU(alpha=0.1))
