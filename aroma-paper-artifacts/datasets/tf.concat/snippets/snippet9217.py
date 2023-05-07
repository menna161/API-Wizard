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


def block_inception_b(inputs, scope=None, reuse=None):
    'Builds Inception-B block for Inception v4 network.'
    with slim.arg_scope([slim.conv2d, slim.avg_pool2d, slim.max_pool2d], stride=1, padding='SAME'):
        with tf.variable_scope(scope, 'BlockInceptionB', [inputs], reuse=reuse):
            with tf.variable_scope('Branch_0'):
                branch_0 = slim.conv2d(inputs, 384, [1, 1], scope='Conv2d_0a_1x1')
            with tf.variable_scope('Branch_1'):
                branch_1 = slim.conv2d(inputs, 192, [1, 1], scope='Conv2d_0a_1x1')
                branch_1 = slim.conv2d(branch_1, 224, [1, 7], scope='Conv2d_0b_1x7')
                branch_1 = slim.conv2d(branch_1, 256, [7, 1], scope='Conv2d_0c_7x1')
            with tf.variable_scope('Branch_2'):
                branch_2 = slim.conv2d(inputs, 192, [1, 1], scope='Conv2d_0a_1x1')
                branch_2 = slim.conv2d(branch_2, 192, [7, 1], scope='Conv2d_0b_7x1')
                branch_2 = slim.conv2d(branch_2, 224, [1, 7], scope='Conv2d_0c_1x7')
                branch_2 = slim.conv2d(branch_2, 224, [7, 1], scope='Conv2d_0d_7x1')
                branch_2 = slim.conv2d(branch_2, 256, [1, 7], scope='Conv2d_0e_1x7')
            with tf.variable_scope('Branch_3'):
                branch_3 = slim.avg_pool2d(inputs, [3, 3], scope='AvgPool_0a_3x3')
                branch_3 = slim.conv2d(branch_3, 128, [1, 1], scope='Conv2d_0b_1x1')
            return tf.concat(axis=3, values=[branch_0, branch_1, branch_2, branch_3])
