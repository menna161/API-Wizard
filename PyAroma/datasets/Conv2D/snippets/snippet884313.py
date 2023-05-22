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


def yolo4_body(inputs, num_anchors, num_classes):
    'Create YOLO_V4 model CNN body in Keras.'
    darknet = Model(inputs, darknet_body(inputs))
    y19 = DarknetConv2D_BN_Leaky(512, (1, 1))(darknet.output)
    y19 = DarknetConv2D_BN_Leaky(1024, (3, 3))(y19)
    y19 = DarknetConv2D_BN_Leaky(512, (1, 1))(y19)
    maxpool1 = MaxPooling2D(pool_size=(13, 13), strides=(1, 1), padding='same')(y19)
    maxpool2 = MaxPooling2D(pool_size=(9, 9), strides=(1, 1), padding='same')(y19)
    maxpool3 = MaxPooling2D(pool_size=(5, 5), strides=(1, 1), padding='same')(y19)
    y19 = Concatenate()([maxpool1, maxpool2, maxpool3, y19])
    y19 = DarknetConv2D_BN_Leaky(512, (1, 1))(y19)
    y19 = DarknetConv2D_BN_Leaky(1024, (3, 3))(y19)
    y19 = DarknetConv2D_BN_Leaky(512, (1, 1))(y19)
    y19_upsample = compose(DarknetConv2D_BN_Leaky(256, (1, 1)), UpSampling2D(2))(y19)
    y38 = DarknetConv2D_BN_Leaky(256, (1, 1))(darknet.layers[204].output)
    y38 = Concatenate()([y38, y19_upsample])
    y38 = DarknetConv2D_BN_Leaky(256, (1, 1))(y38)
    y38 = DarknetConv2D_BN_Leaky(512, (3, 3))(y38)
    y38 = DarknetConv2D_BN_Leaky(256, (1, 1))(y38)
    y38 = DarknetConv2D_BN_Leaky(512, (3, 3))(y38)
    y38 = DarknetConv2D_BN_Leaky(256, (1, 1))(y38)
    y38_upsample = compose(DarknetConv2D_BN_Leaky(128, (1, 1)), UpSampling2D(2))(y38)
    y76 = DarknetConv2D_BN_Leaky(128, (1, 1))(darknet.layers[131].output)
    y76 = Concatenate()([y76, y38_upsample])
    y76 = DarknetConv2D_BN_Leaky(128, (1, 1))(y76)
    y76 = DarknetConv2D_BN_Leaky(256, (3, 3))(y76)
    y76 = DarknetConv2D_BN_Leaky(128, (1, 1))(y76)
    y76 = DarknetConv2D_BN_Leaky(256, (3, 3))(y76)
    y76 = DarknetConv2D_BN_Leaky(128, (1, 1))(y76)
    y76_output = DarknetConv2D_BN_Leaky(256, (3, 3))(y76)
    y76_output = DarknetConv2D((num_anchors * (num_classes + 5)), (1, 1))(y76_output)
    y76_downsample = ZeroPadding2D(((1, 0), (1, 0)))(y76)
    y76_downsample = DarknetConv2D_BN_Leaky(256, (3, 3), strides=(2, 2))(y76_downsample)
    y38 = Concatenate()([y76_downsample, y38])
    y38 = DarknetConv2D_BN_Leaky(256, (1, 1))(y38)
    y38 = DarknetConv2D_BN_Leaky(512, (3, 3))(y38)
    y38 = DarknetConv2D_BN_Leaky(256, (1, 1))(y38)
    y38 = DarknetConv2D_BN_Leaky(512, (3, 3))(y38)
    y38 = DarknetConv2D_BN_Leaky(256, (1, 1))(y38)
    y38_output = DarknetConv2D_BN_Leaky(512, (3, 3))(y38)
    y38_output = DarknetConv2D((num_anchors * (num_classes + 5)), (1, 1))(y38_output)
    y38_downsample = ZeroPadding2D(((1, 0), (1, 0)))(y38)
    y38_downsample = DarknetConv2D_BN_Leaky(512, (3, 3), strides=(2, 2))(y38_downsample)
    y19 = Concatenate()([y38_downsample, y19])
    y19 = DarknetConv2D_BN_Leaky(512, (1, 1))(y19)
    y19 = DarknetConv2D_BN_Leaky(1024, (3, 3))(y19)
    y19 = DarknetConv2D_BN_Leaky(512, (1, 1))(y19)
    y19 = DarknetConv2D_BN_Leaky(1024, (3, 3))(y19)
    y19 = DarknetConv2D_BN_Leaky(512, (1, 1))(y19)
    y19_output = DarknetConv2D_BN_Leaky(1024, (3, 3))(y19)
    y19_output = DarknetConv2D((num_anchors * (num_classes + 5)), (1, 1))(y19_output)
    yolo4_model = Model(inputs, [y19_output, y38_output, y76_output])
    return yolo4_model
