import os
import random
import datetime
import re
import math
import logging
from collections import OrderedDict
import multiprocessing
import numpy as np
import skimage.transform
import tensorflow as tf
import keras
import keras.backend as K
import keras.layers as KL
import keras.engine as KE
import keras.models as KM
from keras.callbacks import Callback
from mrcnn import utils
from distutils.version import LooseVersion
import imgaug
import h5py
from keras.engine import topology
from keras.utils.data_utils import get_file
from mrcnn.parallel_model import ParallelModel


def rpn_graph(feature_map, anchors_per_location, anchor_stride):
    'Builds the computation graph of Region Proposal Network.\n\n    feature_map: backbone features [batch, height, width, depth]\n    anchors_per_location: number of anchors per pixel in the feature map\n    anchor_stride: Controls the density of anchors. Typically 1 (anchors for\n                   every pixel in the feature map), or 2 (every other pixel).\n\n    Returns:\n        rpn_logits: [batch, H, W, 2] Anchor classifier logits (before softmax)\n        rpn_probs: [batch, H, W, 2] Anchor classifier probabilities.\n        rpn_bbox: [batch, H, W, (dy, dx, log(dh), log(dw))] Deltas to be\n                  applied to anchors.\n    '
    shared = KL.Conv2D(512, (3, 3), padding='same', activation='relu', strides=anchor_stride, name='rpn_conv_shared')(feature_map)
    x = KL.Conv2D((2 * anchors_per_location), (1, 1), padding='valid', activation='linear', name='rpn_class_raw')(shared)
    rpn_class_logits = KL.Lambda((lambda t: tf.reshape(t, [tf.shape(t)[0], (- 1), 2])))(x)
    rpn_probs = KL.Activation('softmax', name='rpn_class_xxx')(rpn_class_logits)
    x = KL.Conv2D((anchors_per_location * 4), (1, 1), padding='valid', activation='linear', name='rpn_bbox_pred')(shared)
    rpn_bbox = KL.Lambda((lambda t: tf.reshape(t, [tf.shape(t)[0], (- 1), 4])))(x)
    return [rpn_class_logits, rpn_probs, rpn_bbox]
