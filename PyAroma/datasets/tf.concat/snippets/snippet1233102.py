import tensorflow as tf
import model
import numpy as np


def _get_outputs(self, inputs, input_seq_length=None, is_training=None):
    '\n\t\treshapes the inputs\n\n\t\tArgs:\n\t\t\tinputs: the inputs to concatenate, this is a list of\n\t\t\t\t[batch_size x time x ...] tensors and/or [batch_size x ...] tensors\n\t\t\tinput_seq_length: None\n\t\t\tis_training: None\n\n\t\tReturns:\n\t\t\t- outputs, the reshaped input\n\t\t'
    requested_shape = map(int, self.conf['requested_shape'].split(' '))
    reshape_dim = int(self.conf['reshape_dim'])
    if (len(inputs) > 1):
        raise ('The implementation of Reshaper expects 1 input and not %d' % len(inputs))
    else:
        input = inputs[0]
    with tf.variable_scope(self.scope):
        input_shape = tf.shape(input)
        left_in_shape = input_shape[:reshape_dim]
        right_in_shape = input_shape[(reshape_dim + 1):]
        reshape_dim_shape = tf.concat([left_in_shape, requested_shape, right_in_shape], 0)
        output = tf.reshape(input, reshape_dim_shape)
    return output
