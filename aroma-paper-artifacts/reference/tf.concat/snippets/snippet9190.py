from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
import constants as const
import nets.batch_augment as batch_augment
import utils.os_utils as os_utils
import os


@slim.add_arg_scope
def _conv_block(inputs, num_filters, data_format='NHWC', scope=None, outputs_collections=None):
    with tf.variable_scope(scope, 'conv_blockx', [inputs]) as sc:
        net = inputs
        net = _conv(net, (num_filters * 4), 1, scope='x1')
        net = _conv(net, num_filters, 3, scope='x2')
        if (data_format == 'NHWC'):
            net = tf.concat([inputs, net], axis=3)
        else:
            net = tf.concat([inputs, net], axis=1)
        net = slim.utils.collect_named_outputs(outputs_collections, sc.name, net)
    return net
