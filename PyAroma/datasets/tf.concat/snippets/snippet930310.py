from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import six
import re
import tensorflow as tf
from preprocessing import imagenet_preprocessing
from preprocessing import inception_preprocessing
from preprocessing import reid_preprocessing


def mixup(x, y, alpha=0.2, keep_batch_size=True, y_t=None):
    dist = tf.contrib.distributions.Beta(alpha, alpha)
    (_, h, w, c) = x.get_shape().as_list()
    batch_size = tf.shape(x)[0]
    num_class = y.get_shape().as_list()[1]
    lam1 = dist.sample([(batch_size // 2)])
    if (x.dtype == tf.float16):
        lam1 = tf.cast(lam1, dtype=tf.float16)
        y = tf.cast(y, dtype=tf.float16)
        if (y_t is not None):
            y_t = tf.cast(y_t, dtype=tf.float16)
    (x1, x2) = tf.split(x, 2, axis=0)
    (y1, y2) = tf.split(y, 2, axis=0)
    lam1_x = tf.tile(tf.reshape(lam1, [(batch_size // 2), 1, 1, 1]), [1, h, w, c])
    lam1_y = tf.tile(tf.reshape(lam1, [(batch_size // 2), 1]), [1, num_class])
    mixed_sx1 = ((lam1_x * x1) + ((1.0 - lam1_x) * x2))
    mixed_sy1 = ((lam1_y * y1) + ((1.0 - lam1_y) * y2))
    mixed_sx1 = tf.stop_gradient(mixed_sx1)
    mixed_sy1 = tf.stop_gradient(mixed_sy1)
    if (y_t is not None):
        (y1_t, y2_t) = tf.split(y_t, 2, axis=0)
        mixed_sy1_t = ((lam1_y * y1_t) + ((1.0 - lam1_y) * y2_t))
        mixed_sy1_t = tf.stop_gradient(mixed_sy1_t)
    else:
        mixed_sy1_t = None
    if keep_batch_size:
        lam2 = dist.sample([(batch_size // 2)])
        if (x.dtype == tf.float16):
            lam2 = tf.cast(lam2, dtype=tf.float16)
        lam2_x = tf.tile(tf.reshape(lam2, [(batch_size // 2), 1, 1, 1]), [1, h, w, c])
        lam2_y = tf.tile(tf.reshape(lam2, [(batch_size // 2), 1]), [1, num_class])
        x3 = tf.reverse(x2, [0])
        y3 = tf.reverse(y2, [0])
        mixed_sx2 = ((lam2_x * x1) + ((1.0 - lam2_x) * x3))
        mixed_sy2 = ((lam2_y * y1) + ((1.0 - lam2_y) * y3))
        mixed_sx2 = tf.stop_gradient(mixed_sx2)
        mixed_sy2 = tf.stop_gradient(mixed_sy2)
        mixed_sx1 = tf.concat([mixed_sx1, mixed_sx2], axis=0)
        mixed_sy1 = tf.concat([mixed_sy1, mixed_sy2], axis=0)
        if (y_t is not None):
            y3_t = tf.reverse(y2_t, [0])
            mixed_sy2_t = ((lam2_y * y1) + ((1.0 - lam2_y) * y3_t))
            mixed_sy2_t = tf.stop_gradient(mixed_sy2_t)
            mixed_sy1_t = tf.concat([mixed_sy1_t, mixed_sy2_t], axis=0)
    return (mixed_sx1, mixed_sy1, mixed_sy1_t)
