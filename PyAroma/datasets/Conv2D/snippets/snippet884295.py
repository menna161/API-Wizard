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


def yolo_head(feats, anchors, num_classes, input_shape, calc_loss=False):
    'Convert final layer features to bounding box parameters.'
    num_anchors = len(anchors)
    anchors_tensor = K.reshape(K.constant(anchors), [1, 1, 1, num_anchors, 2])
    grid_shape = K.shape(feats)[1:3]
    grid_y = K.tile(K.reshape(K.arange(0, stop=grid_shape[0]), [(- 1), 1, 1, 1]), [1, grid_shape[1], 1, 1])
    grid_x = K.tile(K.reshape(K.arange(0, stop=grid_shape[1]), [1, (- 1), 1, 1]), [grid_shape[0], 1, 1, 1])
    grid = K.concatenate([grid_x, grid_y])
    grid = K.cast(grid, K.dtype(feats))
    feats = K.reshape(feats, [(- 1), grid_shape[0], grid_shape[1], num_anchors, (num_classes + 5)])
    box_xy = ((K.sigmoid(feats[(..., :2)]) + grid) / K.cast(grid_shape[::(- 1)], K.dtype(feats)))
    box_wh = ((K.exp(feats[(..., 2:4)]) * anchors_tensor) / K.cast(input_shape[::(- 1)], K.dtype(feats)))
    box_confidence = K.sigmoid(feats[(..., 4:5)])
    box_class_probs = K.sigmoid(feats[(..., 5:)])
    if (calc_loss == True):
        return (grid, feats, box_xy, box_wh)
    return (box_xy, box_wh, box_confidence, box_class_probs)
