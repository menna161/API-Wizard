from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import tensorflow as tf


def map_predictor(input_op, predictor_fn, sub_batch_size):
    'Wrapper for tf.map_fn to do batched computation within each map step.'
    num_elements = tf.contrib.framework.nest.flatten(input_op)[0].shape[0].value
    if (num_elements < sub_batch_size):
        return predictor_fn(input_op)
    pad_amount = ((- num_elements) % sub_batch_size)

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
    reshaped_inputs = tf.contrib.framework.nest.map_structure(reshape, input_op)
    mapped_prediction = tf.map_fn(predictor_fn, reshaped_inputs, parallel_iterations=1, back_prop=False, name=None, dtype=tf.float32)
    output_shape = ([(- 1)] + mapped_prediction.shape.as_list()[2:])
    reshaped_output = tf.reshape(mapped_prediction, shape=output_shape)
    if (pad_amount > 0):
        reshaped_output = reshaped_output[(0:(- pad_amount), ...)]
    return reshaped_output
