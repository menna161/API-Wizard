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


def box_iou(b1, b2):
    '\n    Return iou tensor\n\n    Parameters\n    ----------\n    b1: tensor, shape=(i1,...,iN, 4), xywh\n    b2: tensor, shape=(j, 4), xywh\n\n    Returns\n    -------\n    iou: tensor, shape=(i1,...,iN, j)\n    '
    b1 = K.expand_dims(b1, (- 2))
    b1_xy = b1[(..., :2)]
    b1_wh = b1[(..., 2:4)]
    b1_wh_half = (b1_wh / 2.0)
    b1_mins = (b1_xy - b1_wh_half)
    b1_maxes = (b1_xy + b1_wh_half)
    b2 = K.expand_dims(b2, 0)
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
    iou = (intersect_area / ((b1_area + b2_area) - intersect_area))
    return iou
