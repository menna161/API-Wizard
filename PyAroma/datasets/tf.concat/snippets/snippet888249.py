from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
import capslayer as cl
import numpy as np


def space_to_batch_nd(input, kernel_size, strides, name=None):
    ' Space to batch with strides. Different to tf.space_to_batch_nd.\n        for convCapsNet model: memory 4729M, speed 0.165 sec/step, similiar to space_to_batch_nd_v1\n\n    Args:\n        input: A Tensor. N-D with shape input_shape = [batch] + spatial_shape + remaining_shape, where spatial_shape has M dimensions.\n        kernel_size: A sequence of len(spatial_shape)-D positive integers specifying the spatial dimensions of the filters.\n        strides: A sequence of len(spatial_shape)-D positive integers specifying the stride at which to compute output.\n\n    Returns:\n        A Tensor.\n    '
    assert (len(kernel_size) == 3)
    assert (len(strides) == 3)
    name = ('space_to_batch_nd' if (name is None) else name)
    with tf.name_scope(name):
        input_shape = cl.shape(input)
        h_steps = int((((input_shape[1] - kernel_size[0]) / strides[0]) + 1))
        w_steps = int((((input_shape[2] - kernel_size[1]) / strides[1]) + 1))
        d_steps = int((((input_shape[3] - kernel_size[2]) / strides[2]) + 1))
        blocks = []
        for d in range(d_steps):
            d_s = (d * strides[2])
            d_e = (d_s + kernel_size[2])
            h_blocks = []
            for h in range(h_steps):
                h_s = (h * strides[0])
                h_e = (h_s + kernel_size[0])
                w_blocks = []
                for w in range(w_steps):
                    w_s = (w * strides[1])
                    w_e = (w_s + kernel_size[1])
                    block = input[(:, h_s:h_e, w_s:w_e, d_s:d_e)]
                    w_blocks.append(block)
                h_blocks.append(tf.concat(w_blocks, axis=2))
            blocks.append(tf.concat(h_blocks, axis=1))
        return tf.concat(blocks, axis=0)
