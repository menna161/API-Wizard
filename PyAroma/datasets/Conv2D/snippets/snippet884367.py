import sys
import numpy as np
import tensorflow as tf
from keras import backend as K
from keras.layers import Lambda, Reshape, merge
from keras.models import Model
from ..utils import compose
from .keras_darknet19 import DarknetConv2D, DarknetConv2D_BN_Leaky, darknet_body
import tensorflow as tf


def yolo_head(feats, anchors, num_classes):
    'Convert final layer features to bounding box parameters.\n\n    Parameters\n    ----------\n    feats : tensor\n        Final convolutional layer features.\n    anchors : array-like\n        Anchor box widths and heights.\n    num_classes : int\n        Number of target classes.\n\n    Returns\n    -------\n    box_xy : tensor\n        x, y box predictions adjusted by spatial location in conv layer.\n    box_wh : tensor\n        w, h box predictions adjusted by anchors and conv spatial resolution.\n    box_conf : tensor\n        Probability estimate for whether each box contains any object.\n    box_class_pred : tensor\n        Probability distribution estimate for each box over class labels.\n    '
    num_anchors = len(anchors)
    anchors_tensor = K.reshape(K.variable(anchors), [1, 1, 1, num_anchors, 2])
    conv_dims = K.shape(feats)[1:3]
    conv_height_index = K.arange(0, stop=conv_dims[0])
    conv_width_index = K.arange(0, stop=conv_dims[1])
    conv_height_index = K.tile(conv_height_index, [conv_dims[1]])
    conv_width_index = K.tile(K.expand_dims(conv_width_index, 0), [conv_dims[0], 1])
    conv_width_index = K.flatten(K.transpose(conv_width_index))
    conv_index = K.transpose(K.stack([conv_height_index, conv_width_index]))
    conv_index = K.reshape(conv_index, [1, conv_dims[0], conv_dims[1], 1, 2])
    conv_index = K.cast(conv_index, K.dtype(feats))
    feats = K.reshape(feats, [(- 1), conv_dims[0], conv_dims[1], num_anchors, (num_classes + 5)])
    conv_dims = K.cast(K.reshape(conv_dims, [1, 1, 1, 1, 2]), K.dtype(feats))
    box_xy = K.sigmoid(feats[(..., :2)])
    box_wh = K.exp(feats[(..., 2:4)])
    box_confidence = K.sigmoid(feats[(..., 4:5)])
    box_class_probs = K.softmax(feats[(..., 5:)])
    box_xy = ((box_xy + conv_index) / conv_dims)
    box_wh = ((box_wh * anchors_tensor) / conv_dims)
    return (box_xy, box_wh, box_confidence, box_class_probs)
