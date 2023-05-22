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


def create_texture(initial_file):
    if (not (initial_file is None)):
        t = cv2.imread(initial_file)
        p = (np.sum(t, axis=2) > 0)
        t = (((t / 255.0) * 2.0) - 1.0)
        for j in range(3):
            t[(:, :, j)] *= p
        t = np.reshape(t, (1, t.shape[0], t.shape[1], 3))
    else:
        t = np.zeros((1, 1024, 1024, 3))
    texture = tf.get_variable('texture', dtype=tf.float32, initializer=t.astype('float32'))
    return texture
