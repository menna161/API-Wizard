from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import tensorflow as tf
import numpy as np
import argparse
import json
import glob
import random
import collections
import math
import time
from lxml import etree
from random import shuffle


def conv(batch_input, out_channels, stride):
    with tf.variable_scope('conv'):
        in_channels = batch_input.get_shape()[3]
        filter = tf.get_variable('filter', [4, 4, in_channels, out_channels], dtype=tf.float32, initializer=tf.random_normal_initializer(0, 0.02))
        padded_input = tf.pad(batch_input, [[0, 0], [1, 1], [1, 1], [0, 0]], mode='CONSTANT')
        conv = tf.nn.conv2d(padded_input, filter, [1, stride, stride, 1], padding='VALID')
        return conv
