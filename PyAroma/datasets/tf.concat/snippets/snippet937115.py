from __future__ import print_function
import argparse
import os
import numpy as np
import tensorflow as tf
from tensorflow.contrib import slim
import caffe


def square_box(bbox):
    hw = ((bbox[(:, 2:)] - bbox[(:, :2)]) + 1)
    max_side = tf.reduce_max(hw, axis=1, keepdims=True)
    delta = tf.concat([((hw - max_side) * 0.5), ((hw - max_side) * (- 0.5))], axis=1)
    bbox = (bbox + delta)
    return bbox
