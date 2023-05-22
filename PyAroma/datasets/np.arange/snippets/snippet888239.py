from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import capslayer as cl
import tensorflow as tf
from capslayer.core import routing
from capslayer.core import transforming


def dense(inputs, activation, num_outputs, out_caps_dims, routing_method='EMRouting', coordinate_addition=False, reuse=None, name=None):
    'A fully connected capsule layer.\n\n    Args:\n        inputs: A 4-D tensor with shape [batch_size, num_inputs] + in_caps_dims or [batch_size, in_height, in_width, in_channels] + in_caps_dims\n        activation: [batch_size, num_inputs] or [batch_size, in_height, in_width, in_channels]\n        num_outputs: Integer, the number of output capsules in the layer.\n        out_caps_dims: A list with two elements, pose shape of output capsules.\n\n    Returns:\n        pose: A 4-D tensor with shape [batch_size, num_outputs] + out_caps_dims\n        activation: [batch_size, num_outputs]\n    '
    name = ('dense' if (name is None) else name)
    with tf.variable_scope(name) as scope:
        if reuse:
            scope.reuse()
        if (coordinate_addition and (len(inputs.shape) == 6) and (len(activation.shape) == 4)):
            vote = transforming(inputs, num_outputs=num_outputs, out_caps_dims=out_caps_dims)
            with tf.name_scope('coodinate_addition'):
                (batch_size, in_height, in_width, in_channels, _, out_caps_height, out_caps_width) = cl.shape(vote)
                num_inputs = ((in_height * in_width) * in_channels)
                zeros = np.zeros((in_height, (out_caps_width - 1)))
                coord_offset_h = ((np.arange(in_height) + 0.5) / in_height).reshape([in_height, 1])
                coord_offset_h = np.concatenate([zeros, coord_offset_h], axis=(- 1))
                zeros = np.zeros(((out_caps_height - 1), out_caps_width))
                coord_offset_h = np.stack([np.concatenate([coord_offset_h[(i:(i + 1), :)], zeros], axis=0) for i in range(in_height)], axis=0)
                coord_offset_h = coord_offset_h.reshape((1, in_height, 1, 1, 1, out_caps_height, out_caps_width))
                zeros = np.zeros((1, in_width))
                coord_offset_w = ((np.arange(in_width) + 0.5) / in_width).reshape([1, in_width])
                coord_offset_w = np.concatenate([zeros, coord_offset_w, zeros, zeros], axis=0)
                zeros = np.zeros((out_caps_height, (out_caps_width - 1)))
                coord_offset_w = np.stack([np.concatenate([zeros, coord_offset_w[(:, i:(i + 1))]], axis=1) for i in range(in_width)], axis=0)
                coord_offset_w = coord_offset_w.reshape((1, 1, in_width, 1, 1, out_caps_height, out_caps_width))
                vote = (vote + tf.constant((coord_offset_h + coord_offset_w), dtype=tf.float32))
                vote = tf.reshape(vote, shape=([batch_size, num_inputs, num_outputs] + out_caps_dims))
                activation = tf.reshape(activation, shape=[batch_size, num_inputs])
        elif ((len(inputs.shape) == 4) and (len(activation.shape) == 2)):
            vote = transforming(inputs, num_outputs=num_outputs, out_caps_dims=out_caps_dims)
        else:
            raise TypeError('Wrong rank for inputs or activation')
        (pose, activation) = routing(vote, activation, routing_method)
        assert (len(pose.shape) == 4)
        assert (len(activation.shape) == 2)
    return (pose, activation)
