from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import tensorflow as tf
import argparse
import glob
import cv2
import numpy as np
import pickle
import random
import collections
import time
from tensorflow.python.client import device_lib


def discrim_conv_mask(batch_input, stride):
    padded_input = tf.pad(batch_input, [[0, 0], [1, 1], [1, 1], [0, 0]], mode='CONSTANT')
    return tf.layers.conv2d(padded_input, 1, kernel_size=4, strides=(stride, stride), padding='valid', kernel_initializer=tf.constant_initializer((1.0 / 16)))
