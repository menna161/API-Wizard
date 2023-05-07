from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
from absl import flags
from tensorflow.python.ops import control_flow_ops
from tensorflow.python.ops import random_ops


def distort_color_fast(image, scope=None):
    'Distort the color of a Tensor image.\n\n  Distort brightness and chroma values of input image\n\n  Args:\n    image: 3-D Tensor containing single image in [0, 1].\n    scope: Optional scope for name_scope.\n  Returns:\n    3-D Tensor color-distorted image on range [0, 1]\n  '
    with tf.name_scope(scope, 'distort_color', [image]):
        br_delta = random_ops.random_uniform([], ((- 32.0) / 255.0), (32.0 / 255.0), seed=None)
        cb_factor = random_ops.random_uniform([], (- FLAGS.cb_distortion_range), FLAGS.cb_distortion_range, seed=None)
        cr_factor = random_ops.random_uniform([], (- FLAGS.cr_distortion_range), FLAGS.cr_distortion_range, seed=None)
        channels = tf.split(axis=2, num_or_size_splits=3, value=image)
        red_offset = ((1.402 * cr_factor) + br_delta)
        green_offset = ((((- 0.344136) * cb_factor) - (0.714136 * cr_factor)) + br_delta)
        blue_offset = ((1.772 * cb_factor) + br_delta)
        channels[0] += red_offset
        channels[1] += green_offset
        channels[2] += blue_offset
        image = tf.concat(axis=2, values=channels)
        image = tf.minimum(tf.maximum(image, 0.0), 1.0)
        return image
