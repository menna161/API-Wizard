from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import inspect
import math
import tensorflow as tf


def build_lut(histo, step):
    lut = ((tf.cumsum(histo) + (step // 2)) // step)
    lut = tf.concat([[0], lut[:(- 1)]], 0)
    return tf.clip_by_value(lut, 0, 255)
