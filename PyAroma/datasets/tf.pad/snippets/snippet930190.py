from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf


def fixed_padding(inputs, kernel_size, data_format):
    "Pads the input along the spatial dimensions independently of input size.\n\n  Args:\n    inputs: A tensor of size [batch, channels, height_in, width_in] or\n      [batch, height_in, width_in, channels] depending on data_format.\n    kernel_size: The kernel to be used in the conv2d or max_pool2d operation.\n                 Should be a positive integer.\n    data_format: The input format ('channels_last' or 'channels_first').\n\n  Returns:\n    A tensor with the same format as the input with the data either intact\n    (if kernel_size == 1) or padded (if kernel_size > 1).\n  "
    pad_total = (kernel_size - 1)
    pad_beg = (pad_total // 2)
    pad_end = (pad_total - pad_beg)
    if (data_format == 'channels_first'):
        padded_inputs = tf.pad(inputs, [[0, 0], [0, 0], [pad_beg, pad_end], [pad_beg, pad_end]])
    else:
        padded_inputs = tf.pad(inputs, [[0, 0], [pad_beg, pad_end], [pad_beg, pad_end], [0, 0]])
    return padded_inputs
