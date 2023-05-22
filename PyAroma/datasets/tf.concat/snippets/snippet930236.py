from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import inspect
import math
import tensorflow as tf


def wrap(image):
    "Returns 'image' with an extra channel set to all 1s."
    shape = tf.shape(image)
    extended_channel = tf.ones([shape[0], shape[1], 1], image.dtype)
    extended = tf.concat([image, extended_channel], 2)
    return extended
