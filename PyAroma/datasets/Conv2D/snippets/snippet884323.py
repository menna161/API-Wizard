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


def box_diou(b1, b2):
    '\n    Calculate DIoU loss on anchor boxes\n    Reference Paper:\n        "Distance-IoU Loss: Faster and Better Learning for Bounding Box Regression"\n        https://arxiv.org/abs/1911.08287\n\n    Parameters\n    ----------\n    b1: tensor, shape=(batch, feat_w, feat_h, anchor_num, 4), xywh\n    b2: tensor, shape=(batch, feat_w, feat_h, anchor_num, 4), xywh\n\n    Returns\n    -------\n    diou: tensor, shape=(batch, feat_w, feat_h, anchor_num, 1)\n    '
    b1_xy = b1[(..., :2)]
    b1_wh = b1[(..., 2:4)]
    b1_wh_half = (b1_wh / 2.0)
    b1_mins = (b1_xy - b1_wh_half)
    b1_maxes = (b1_xy + b1_wh_half)
    b2_xy = b2[(..., :2)]
    b2_wh = b2[(..., 2:4)]
    b2_wh_half = (b2_wh / 2.0)
    b2_mins = (b2_xy - b2_wh_half)
    b2_maxes = (b2_xy + b2_wh_half)
    intersect_mins = K.maximum(b1_mins, b2_mins)
    intersect_maxes = K.minimum(b1_maxes, b2_maxes)
    intersect_wh = K.maximum((intersect_maxes - intersect_mins), 0.0)
    intersect_area = (intersect_wh[(..., 0)] * intersect_wh[(..., 1)])
    b1_area = (b1_wh[(..., 0)] * b1_wh[(..., 1)])
    b2_area = (b2_wh[(..., 0)] * b2_wh[(..., 1)])
    union_area = ((b1_area + b2_area) - intersect_area)
    iou = (intersect_area / (union_area + K.epsilon()))
    center_distance = K.sum(K.square((b1_xy - b2_xy)), axis=(- 1))
    enclose_mins = K.minimum(b1_mins, b2_mins)
    enclose_maxes = K.maximum(b1_maxes, b2_maxes)
    enclose_wh = K.maximum((enclose_maxes - enclose_mins), 0.0)
    enclose_diagonal = K.sum(K.square(enclose_wh), axis=(- 1))
    diou = (iou - ((1.0 * center_distance) / (enclose_diagonal + K.epsilon())))
    diou = K.expand_dims(diou, (- 1))
    return diou
