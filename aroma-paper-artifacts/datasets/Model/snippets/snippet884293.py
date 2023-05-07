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


def yolo_body(inputs, num_anchors, num_classes):
    'Create YOLO_V3 model CNN body in Keras.'
    darknet = Model(inputs, darknet_body(inputs))
    (x, y1) = make_last_layers(darknet.output, 512, (num_anchors * (num_classes + 5)))
    x = compose(DarknetConv2D_BN_Leaky(256, (1, 1)), UpSampling2D(2))(x)
    x = Concatenate()([x, darknet.layers[152].output])
    (x, y2) = make_last_layers(x, 256, (num_anchors * (num_classes + 5)))
    x = compose(DarknetConv2D_BN_Leaky(128, (1, 1)), UpSampling2D(2))(x)
    x = Concatenate()([x, darknet.layers[92].output])
    (x, y3) = make_last_layers(x, 128, (num_anchors * (num_classes + 5)))
    return Model(inputs, [y1, y2, y3])
