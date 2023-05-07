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


def block_inception_c(inputs, scope=None, reuse=None):
    'Builds Inception-C block for Inception v4 network.'
    with slim.arg_scope([slim.conv2d, slim.avg_pool2d, slim.max_pool2d], stride=1, padding='SAME'):
        with tf.variable_scope(scope, 'BlockInceptionC', [inputs], reuse=reuse):
            with tf.variable_scope('Branch_0'):
                branch_0 = slim.conv2d(inputs, 256, [1, 1], scope='Conv2d_0a_1x1')
            with tf.variable_scope('Branch_1'):
                branch_1 = slim.conv2d(inputs, 384, [1, 1], scope='Conv2d_0a_1x1')
                branch_1 = tf.concat(axis=3, values=[slim.conv2d(branch_1, 256, [1, 3], scope='Conv2d_0b_1x3'), slim.conv2d(branch_1, 256, [3, 1], scope='Conv2d_0c_3x1')])
            with tf.variable_scope('Branch_2'):
                branch_2 = slim.conv2d(inputs, 384, [1, 1], scope='Conv2d_0a_1x1')
                branch_2 = slim.conv2d(branch_2, 448, [3, 1], scope='Conv2d_0b_3x1')
                branch_2 = slim.conv2d(branch_2, 512, [1, 3], scope='Conv2d_0c_1x3')
                branch_2 = tf.concat(axis=3, values=[slim.conv2d(branch_2, 256, [1, 3], scope='Conv2d_0d_1x3'), slim.conv2d(branch_2, 256, [3, 1], scope='Conv2d_0e_3x1')])
            with tf.variable_scope('Branch_3'):
                branch_3 = slim.avg_pool2d(inputs, [3, 3], scope='AvgPool_0a_3x3')
                branch_3 = slim.conv2d(branch_3, 256, [1, 1], scope='Conv2d_0b_1x1')
            return tf.concat(axis=3, values=[branch_0, branch_1, branch_2, branch_3])
