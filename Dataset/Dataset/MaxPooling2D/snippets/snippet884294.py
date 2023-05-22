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


def tiny_yolo_body(inputs, num_anchors, num_classes):
    'Create Tiny YOLO_v3 model CNN body in keras.'
    x1 = compose(DarknetConv2D_BN_Leaky(16, (3, 3)), MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'), DarknetConv2D_BN_Leaky(32, (3, 3)), MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'), DarknetConv2D_BN_Leaky(64, (3, 3)), MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'), DarknetConv2D_BN_Leaky(128, (3, 3)), MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'), DarknetConv2D_BN_Leaky(256, (3, 3)))(inputs)
    x2 = compose(MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'), DarknetConv2D_BN_Leaky(512, (3, 3)), MaxPooling2D(pool_size=(2, 2), strides=(1, 1), padding='same'), DarknetConv2D_BN_Leaky(1024, (3, 3)), DarknetConv2D_BN_Leaky(256, (1, 1)))(x1)
    y1 = compose(DarknetConv2D_BN_Leaky(512, (3, 3)), DarknetConv2D((num_anchors * (num_classes + 5)), (1, 1)))(x2)
    x2 = compose(DarknetConv2D_BN_Leaky(128, (1, 1)), UpSampling2D(2))(x2)
    y2 = compose(Concatenate(), DarknetConv2D_BN_Leaky(256, (3, 3)), DarknetConv2D((num_anchors * (num_classes + 5)), (1, 1)))([x2, x1])
    return Model(inputs, [y1, y2])
