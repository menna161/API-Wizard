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


def fpn_classifier_graph(rois, feature_maps, image_meta, pool_size, num_classes, train_bn=True):
    'Builds the computation graph of the feature pyramid network classifier\n    and regressor heads.\n\n    rois: [batch, num_rois, (y1, x1, y2, x2)] Proposal boxes in normalized\n          coordinates.\n    feature_maps: List of feature maps from diffent layers of the pyramid,\n                  [P2, P3, P4, P5]. Each has a different resolution.\n    - image_meta: [batch, (meta data)] Image details. See compose_image_meta()\n    pool_size: The width of the square feature map generated from ROI Pooling.\n    num_classes: number of classes, which determines the depth of the results\n    train_bn: Boolean. Train or freeze Batch Norm layres\n\n    Returns:\n        logits: [N, NUM_CLASSES] classifier logits (before softmax)\n        probs: [N, NUM_CLASSES] classifier probabilities\n        bbox_deltas: [N, (dy, dx, log(dh), log(dw))] Deltas to apply to\n                     proposal boxes\n    '
    x = PyramidROIAlign([pool_size, pool_size], name='roi_align_classifier')(([rois, image_meta] + feature_maps))
    x = KL.TimeDistributed(KL.Conv2D(1024, (pool_size, pool_size), padding='valid'), name='mrcnn_class_conv1')(x)
    x = KL.TimeDistributed(BatchNorm(), name='mrcnn_class_bn1')(x, training=train_bn)
    x = KL.Activation('relu')(x)
    x = KL.TimeDistributed(KL.Conv2D(1024, (1, 1)), name='mrcnn_class_conv2')(x)
    x = KL.TimeDistributed(BatchNorm(), name='mrcnn_class_bn2')(x, training=train_bn)
    x = KL.Activation('relu')(x)
    shared = KL.Lambda((lambda x: K.squeeze(K.squeeze(x, 3), 2)), name='pool_squeeze')(x)
    mrcnn_class_logits = KL.TimeDistributed(KL.Dense(num_classes), name='mrcnn_class_logits')(shared)
    mrcnn_probs = KL.TimeDistributed(KL.Activation('softmax'), name='mrcnn_class')(mrcnn_class_logits)
    x = KL.TimeDistributed(KL.Dense((num_classes * 4), activation='linear'), name='mrcnn_bbox_fc')(shared)
    s = K.int_shape(x)
    mrcnn_bbox = KL.Reshape((s[1], num_classes, 4), name='mrcnn_bbox')(x)
    return (mrcnn_class_logits, mrcnn_probs, mrcnn_bbox)
