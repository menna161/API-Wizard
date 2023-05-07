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


def det_conv_block(input_tensor, kernel_size, filters, stage, block, strides=(2, 2), use_bias=True, train_bn=True):
    "conv_block is the block that has a conv layer at shortcut\n    # Arguments\n        input_tensor: input tensor\n        kernel_size: defualt 3, the kernel size of middle conv layer at main path\n        filters: list of integers, the nb_filters of 3 conv layer at main path\n        stage: integer, current stage label, used for generating layer names\n        block: 'a','b'..., current block label, used for generating layer names\n    Note that from stage 3, the first conv layer at main path is with subsample=(2,2)\n    And the shortcut should have subsample=(2,2) as well\n    "
    (nb_filter1, nb_filter2, nb_filter3) = filters
    conv_name_base = ((('res' + str(stage)) + block) + '_branch')
    bn_name_base = ((('bn' + str(stage)) + block) + '_branch')
    x = KL.Conv2D(nb_filter1, (1, 1), strides=strides, name=(conv_name_base + '2a'), use_bias=use_bias)(input_tensor)
    x = BatchNorm(axis=3, name=(bn_name_base + '2a'))(x)
    x = KL.Activation('relu')(x)
    x = KL.Conv2D(nb_filter2, (kernel_size, kernel_size), padding='same', name=(conv_name_base + '2b'), use_bias=use_bias, dilation_rate=2)(x)
    x = BatchNorm(axis=3, name=(bn_name_base + '2b'))(x)
    x = KL.Activation('relu')(x)
    x = KL.Conv2D(nb_filter3, (1, 1), name=(conv_name_base + '2c'), use_bias=use_bias)(x)
    x = BatchNorm(axis=3, name=(bn_name_base + '2c'))(x)
    shortcut = KL.Conv2D(nb_filter3, (1, 1), strides=strides, name=(conv_name_base + '1'), use_bias=use_bias)(input_tensor)
    shortcut = BatchNorm(axis=3, name=(bn_name_base + '1'))(shortcut)
    x = KL.Add()([x, shortcut])
    x = KL.Activation('relu', name=((('res' + str(stage)) + block) + '_out'))(x)
    return x
