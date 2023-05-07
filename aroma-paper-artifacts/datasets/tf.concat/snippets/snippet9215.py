from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
import tensorflow as tf
import constants as const
import nets.batch_augment as batch_augment
import utils.os_utils as os_utils
import os
from nets import inception_utils


def block_inception_a(inputs, scope=None, reuse=None):
    'Builds Inception-A block for Inception v4 network.'
    with slim.arg_scope([slim.conv2d, slim.avg_pool2d, slim.max_pool2d], stride=1, padding='SAME'):
        with tf.variable_scope(scope, 'BlockInceptionA', [inputs], reuse=reuse):
            with tf.variable_scope('Branch_0'):
                branch_0 = slim.conv2d(inputs, 96, [1, 1], scope='Conv2d_0a_1x1')
            with tf.variable_scope('Branch_1'):
                branch_1 = slim.conv2d(inputs, 64, [1, 1], scope='Conv2d_0a_1x1')
                branch_1 = slim.conv2d(branch_1, 96, [3, 3], scope='Conv2d_0b_3x3')
            with tf.variable_scope('Branch_2'):
                branch_2 = slim.conv2d(inputs, 64, [1, 1], scope='Conv2d_0a_1x1')
                branch_2 = slim.conv2d(branch_2, 96, [3, 3], scope='Conv2d_0b_3x3')
                branch_2 = slim.conv2d(branch_2, 96, [3, 3], scope='Conv2d_0c_3x3')
            with tf.variable_scope('Branch_3'):
                branch_3 = slim.avg_pool2d(inputs, [3, 3], scope='AvgPool_0a_3x3')
                branch_3 = slim.conv2d(branch_3, 96, [1, 1], scope='Conv2d_0b_1x1')
            return tf.concat(axis=3, values=[branch_0, branch_1, branch_2, branch_3])
