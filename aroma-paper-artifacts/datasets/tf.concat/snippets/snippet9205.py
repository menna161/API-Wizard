from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf


def _mean_image_subtraction(image, means):
    "Subtracts the given means from each image channel.\n\n  For example:\n    means = [123.68, 116.779, 103.939]\n    image = _mean_image_subtraction(image, means)\n\n  Note that the rank of `image` must be known.\n\n  Args:\n    image: a tensor of size [height, width, C].\n    means: a C-vector of values to subtract from each channel.\n\n  Returns:\n    the centered image.\n\n  Raises:\n    ValueError: If the rank of `image` is unknown, if `image` has a rank other\n      than three or if the number of channels in `image` doesn't match the\n      number of values in `means`.\n  "
    if (image.get_shape().ndims != 3):
        raise ValueError('Input must be of size [height, width, C>0]')
    num_channels = image.get_shape().as_list()[(- 1)]
    if (len(means) != num_channels):
        raise ValueError('len(means) must match the number of channels')
    channels = tf.split(axis=2, num_or_size_splits=num_channels, value=image)
    for i in range(num_channels):
        channels[i] -= means[i]
    return tf.concat(axis=2, values=channels)
