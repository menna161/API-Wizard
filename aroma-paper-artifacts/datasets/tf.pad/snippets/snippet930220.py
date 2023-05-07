from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import inspect
import math
import tensorflow as tf


def cutout(image, pad_size, replace=0):
    'Apply cutout (https://arxiv.org/abs/1708.04552) to image.\n\n  This operation applies a (2*pad_size x 2*pad_size) mask of zeros to\n  a random location within `img`. The pixel values filled in will be of the\n  value `replace`. The located where the mask will be applied is randomly\n  chosen uniformly over the whole image.\n\n  Args:\n    image: An image Tensor of type uint8.\n    pad_size: Specifies how big the zero mask that will be generated is that\n      is applied to the image. The mask will be of size\n      (2*pad_size x 2*pad_size).\n    replace: What pixel value to fill in the image in the area that has\n      the cutout mask applied to it.\n\n  Returns:\n    An image Tensor that is of type uint8.\n  '
    image_height = tf.shape(image)[0]
    image_width = tf.shape(image)[1]
    cutout_center_height = tf.random_uniform(shape=[], minval=0, maxval=image_height, dtype=tf.int32)
    cutout_center_width = tf.random_uniform(shape=[], minval=0, maxval=image_width, dtype=tf.int32)
    lower_pad = tf.maximum(0, (cutout_center_height - pad_size))
    upper_pad = tf.maximum(0, ((image_height - cutout_center_height) - pad_size))
    left_pad = tf.maximum(0, (cutout_center_width - pad_size))
    right_pad = tf.maximum(0, ((image_width - cutout_center_width) - pad_size))
    cutout_shape = [(image_height - (lower_pad + upper_pad)), (image_width - (left_pad + right_pad))]
    padding_dims = [[lower_pad, upper_pad], [left_pad, right_pad]]
    mask = tf.pad(tf.zeros(cutout_shape, dtype=image.dtype), padding_dims, constant_values=1)
    mask = tf.expand_dims(mask, (- 1))
    mask = tf.tile(mask, [1, 1, 3])
    image = tf.where(tf.equal(mask, 0), (tf.ones_like(image, dtype=image.dtype) * replace), image)
    return image
