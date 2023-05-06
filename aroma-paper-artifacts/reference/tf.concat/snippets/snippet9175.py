import tensorflow as tf
import math
import constants as const
import numpy as np
import imageio
from pydoc import locate
from tensorflow.python.ops import control_flow_ops


def _std_image_normalize(image, stds):
    "Subtracts the given means from each image channel.\n\n  For example:\n    means = [123.68, 116.779, 103.939]\n    image = _mean_image_subtraction(image, means)\n\n  Note that the rank of `image` must be known.\n\n  Args:\n    image: a tensor of size [height, width, C].\n    means: a C-vector of values to subtract from each channel.\n\n  Returns:\n    the centered image.\n\n  Raises:\n    ValueError: If the rank of `image` is unknown, if `image` has a rank other\n      than three or if the number of channels in `image` doesn't match the\n      number of values in `means`.\n  "
    num_channels = image.get_shape().as_list()[(- 1)]
    if (len(stds) != num_channels):
        raise ValueError('len(means) must match the number of channels')
    channels = tf.split(axis=3, num_or_size_splits=num_channels, value=image)
    for i in range(num_channels):
        channels[i] /= stds[i]
    return tf.concat(axis=3, values=channels)
