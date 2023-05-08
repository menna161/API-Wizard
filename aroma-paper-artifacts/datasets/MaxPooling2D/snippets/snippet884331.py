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


def loop_body(b, ignore_mask):
    true_box = tf.boolean_mask(y_true[l][(b, ..., 0:4)], object_mask_bool[(b, ..., 0)])
    iou = box_iou(pred_box[b], true_box)
    best_iou = K.max(iou, axis=(- 1))
    ignore_mask = ignore_mask.write(b, K.cast((best_iou < ignore_thresh), K.dtype(true_box)))
    return ((b + 1), ignore_mask)
