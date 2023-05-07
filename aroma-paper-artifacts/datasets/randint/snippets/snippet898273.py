import cv2
import numpy as np
import tensorflow as tf
from logging import exception
import math
import scipy.stats as st
import os
import urllib
import scipy
from scipy import io
from enum import Enum
from easydict import EasyDict as edict


def bbox2mask(bbox, config, name='mask'):
    'Generate mask tensor from bbox.\n\n    Args:\n        bbox: configuration tuple, (top, left, height, width)\n        config: Config should have configuration including IMG_SHAPES,\n            MAX_DELTA_HEIGHT, MAX_DELTA_WIDTH.\n\n    Returns:\n        tf.Tensor: output with shape [1, H, W, 1]\n\n    '

    def npmask(bbox, height, width, delta_h, delta_w):
        mask = np.zeros((1, height, width, 1), np.float32)
        h = np.random.randint(((delta_h // 2) + 1))
        w = np.random.randint(((delta_w // 2) + 1))
        mask[(:, (bbox[0] + h):((bbox[0] + bbox[2]) - h), (bbox[1] + w):((bbox[1] + bbox[3]) - w), :)] = 1.0
        return mask
    with tf.variable_scope(name), tf.device('/cpu:0'):
        img_shape = config.img_shapes
        height = img_shape[0]
        width = img_shape[1]
        mask = tf.py_func(npmask, [bbox, height, width, config.max_delta_shapes[0], config.max_delta_shapes[1]], tf.float32, stateful=False)
        mask.set_shape((([1] + [height, width]) + [1]))
    return mask
