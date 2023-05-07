import sys
import numpy as np
import tensorflow as tf
from keras import backend as K
from keras.layers import Lambda, Reshape, merge
from keras.models import Model
from ..utils import compose
from .keras_darknet19 import DarknetConv2D, DarknetConv2D_BN_Leaky, darknet_body
import tensorflow as tf


def yolo_body(inputs, num_anchors, num_classes):
    'Create YOLO_V2 model CNN body in Keras.'
    darknet = Model(inputs, darknet_body()(inputs))
    conv13 = darknet.get_layer('batchnormalization_13').output
    conv20 = compose(DarknetConv2D_BN_Leaky(1024, 3, 3), DarknetConv2D_BN_Leaky(1024, 3, 3))(darknet.output)
    conv13_reshaped = Lambda(space_to_depth_x2, output_shape=space_to_depth_x2_output_shape, name='space_to_depth')(conv13)
    x = merge([conv13_reshaped, conv20], mode='concat')
    x = DarknetConv2D_BN_Leaky(1024, 3, 3)(x)
    x = DarknetConv2D((num_anchors * (num_classes + 5)), 1, 1)(x)
    return Model(inputs, x)
