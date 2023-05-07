from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import inspect
import math
import tensorflow as tf


def unwrap(image, replace):
    "Unwraps an image produced by wrap.\n\n  Where there is a 0 in the last channel for every spatial position,\n  the rest of the three channels in that spatial dimension are grayed\n  (set to 128).  Operations like translate and shear on a wrapped\n  Tensor will leave 0s in empty locations.  Some transformations look\n  at the intensity of values to do preprocessing, and we want these\n  empty pixels to assume the 'average' value, rather than pure black.\n\n\n  Args:\n    image: A 3D Image Tensor with 4 channels.\n    replace: A one or three value 1D tensor to fill empty pixels.\n\n  Returns:\n    image: A 3D image Tensor with 3 channels.\n  "
    image_shape = tf.shape(image)
    flattened_image = tf.reshape(image, [(- 1), image_shape[2]])
    alpha_channel = flattened_image[(:, 3)]
    replace = tf.concat([replace, tf.ones([1], image.dtype)], 0)
    flattened_image = tf.where(tf.equal(alpha_channel, 0), (tf.ones_like(flattened_image, dtype=image.dtype) * replace), flattened_image)
    image = tf.reshape(flattened_image, image_shape)
    image = tf.slice(image, [0, 0, 0], [image_shape[0], image_shape[1], 3])
    return image
