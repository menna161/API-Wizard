from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import tensorflow as tf


def reshape(tensor):
    'Reshape into batches of sub-batches.'
    pad_shape = tensor.shape.as_list()
    pad_shape[0] = pad_amount
    padding = tf.zeros(shape=pad_shape, dtype=tensor.dtype)
    tensor = tf.concat([tensor, padding], axis=0)
    if ((tensor.shape[0].value % sub_batch_size) != 0):
        raise ValueError(('Incorrent padding size: %d does not divide %d' % (sub_batch_size, tensor.shape[0].value)))
    shape = tensor.shape.as_list()
    output_shape = ([(- 1), sub_batch_size] + shape[1:])
    return tf.reshape(tensor, shape=output_shape)
