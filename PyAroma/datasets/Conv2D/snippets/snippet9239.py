from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import collections
import tensorflow as tf


def conv2d_same(inputs, num_outputs, kernel_size, stride, rate=1, scope=None):
    "Strided 2-D convolution with 'SAME' padding.\n\n  When stride > 1, then we do explicit zero-padding, followed by conv2d with\n  'VALID' padding.\n\n  Note that\n\n     net = conv2d_same(inputs, num_outputs, 3, stride=stride)\n\n  is equivalent to\n\n     net = slim.conv2d(inputs, num_outputs, 3, stride=1, padding='SAME')\n     net = subsample(net, factor=stride)\n\n  whereas\n\n     net = slim.conv2d(inputs, num_outputs, 3, stride=stride, padding='SAME')\n\n  is different when the input's height or width is even, which is why we add the\n  current function. For more details, see ResnetUtilsTest.testConv2DSameEven().\n\n  Args:\n    inputs: A 4-D tensor of size [batch, height_in, width_in, channels].\n    num_outputs: An integer, the number of output filters.\n    kernel_size: An int with the kernel_size of the filters.\n    stride: An integer, the output stride.\n    rate: An integer, rate for atrous convolution.\n    scope: Scope.\n\n  Returns:\n    output: A 4-D tensor of size [batch, height_out, width_out, channels] with\n      the convolution output.\n  "
    if (stride == 1):
        return slim.conv2d(inputs, num_outputs, kernel_size, stride=1, rate=rate, padding='SAME', scope=scope)
    else:
        kernel_size_effective = (kernel_size + ((kernel_size - 1) * (rate - 1)))
        pad_total = (kernel_size_effective - 1)
        pad_beg = (pad_total // 2)
        pad_end = (pad_total - pad_beg)
        inputs = tf.pad(inputs, [[0, 0], [pad_beg, pad_end], [pad_beg, pad_end], [0, 0]])
        return slim.conv2d(inputs, num_outputs, kernel_size, stride=stride, rate=rate, padding='VALID', scope=scope)
