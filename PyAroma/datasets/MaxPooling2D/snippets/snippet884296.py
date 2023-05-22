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


def yolo_correct_boxes(box_xy, box_wh, input_shape, image_shape):
    'Get corrected boxes'
    box_yx = box_xy[(..., ::(- 1))]
    box_hw = box_wh[(..., ::(- 1))]
    input_shape = K.cast(input_shape, K.dtype(box_yx))
    image_shape = K.cast(image_shape, K.dtype(box_yx))
    new_shape = K.round((image_shape * K.min((input_shape / image_shape))))
    offset = (((input_shape - new_shape) / 2.0) / input_shape)
    scale = (input_shape / new_shape)
    box_yx = ((box_yx - offset) * scale)
    box_hw *= scale
    box_mins = (box_yx - (box_hw / 2.0))
    box_maxes = (box_yx + (box_hw / 2.0))
    boxes = K.concatenate([box_mins[(..., 0:1)], box_mins[(..., 1:2)], box_maxes[(..., 0:1)], box_maxes[(..., 1:2)]])
    boxes *= K.concatenate([image_shape, image_shape])
    return boxes
