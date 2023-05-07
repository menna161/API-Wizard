from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from collections import namedtuple
import functools
import tensorflow as tf
import constants as const
import nets.batch_augment as batch_augment
import utils.os_utils as os_utils
import os


def _fixed_padding(inputs, kernel_size, rate=1):
    "Pads the input along the spatial dimensions independently of input size.\n\n  Pads the input such that if it was used in a convolution with 'VALID' padding,\n  the output would have the same dimensions as if the unpadded input was used\n  in a convolution with 'SAME' padding.\n\n  Args:\n    inputs: A tensor of size [batch, height_in, width_in, channels].\n    kernel_size: The kernel to be used in the conv2d or max_pool2d operation.\n    rate: An integer, rate for atrous convolution.\n\n  Returns:\n    output: A tensor of size [batch, height_out, width_out, channels] with the\n      input, either intact (if kernel_size == 1) or padded (if kernel_size > 1).\n  "
    kernel_size_effective = [(kernel_size[0] + ((kernel_size[0] - 1) * (rate - 1))), (kernel_size[0] + ((kernel_size[0] - 1) * (rate - 1)))]
    pad_total = [(kernel_size_effective[0] - 1), (kernel_size_effective[1] - 1)]
    pad_beg = [(pad_total[0] // 2), (pad_total[1] // 2)]
    pad_end = [(pad_total[0] - pad_beg[0]), (pad_total[1] - pad_beg[1])]
    padded_inputs = tf.pad(inputs, [[0, 0], [pad_beg[0], pad_end[0]], [pad_beg[1], pad_end[1]], [0, 0]])
    return padded_inputs
