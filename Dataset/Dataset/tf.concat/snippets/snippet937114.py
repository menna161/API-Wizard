from __future__ import print_function
import argparse
import os
import numpy as np
import tensorflow as tf
from tensorflow.contrib import slim
import caffe


def regress_box(bbox, reg):
    hw = (bbox[(:, 2:)] - bbox[(:, :2)])
    hw = tf.concat([hw, hw], axis=1)
    bbox = (bbox + (hw * reg))
    return bbox
