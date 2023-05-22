from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
from tensorflow.python.ops import control_flow_ops
from preprocessing import autoaugment


def pad_shorter(image):
    shape = tf.shape(image)
    (height, width) = (shape[0], shape[1])
    larger_dim = tf.maximum(height, width)
    h1 = ((larger_dim - height) // 2)
    h2 = ((larger_dim - height) - h1)
    w1 = tf.maximum(((larger_dim - width) // 2), 0)
    w2 = ((larger_dim - width) - w1)
    pad_shape = [[h1, h2], [w1, w2], [0, 0]]
    return tf.pad(image, pad_shape)
