import sys
import numpy as np
import tensorflow as tf
from keras import backend as K
from keras.layers import Lambda, Reshape, merge
from keras.models import Model
from ..utils import compose
from .keras_darknet19 import DarknetConv2D, DarknetConv2D_BN_Leaky, darknet_body
import tensorflow as tf


def yolo_boxes_to_corners(box_xy, box_wh):
    'Convert YOLO box predictions to bounding box corners.'
    box_mins = (box_xy - (box_wh / 2.0))
    box_maxes = (box_xy + (box_wh / 2.0))
    return K.concatenate([box_mins[(..., 1:2)], box_mins[(..., 0:1)], box_maxes[(..., 1:2)], box_maxes[(..., 0:1)]])
