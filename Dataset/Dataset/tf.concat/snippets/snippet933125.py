import tensorflow as tf
import numpy as np
import os
from PIL import Image
import scipy.misc as misc


def discriminator(self, inputs, inputs_condition):
    inputs = tf.concat([inputs, inputs_condition], axis=3)
    inputs = tf.random_crop(inputs, [1, 70, 70, 2])
    with tf.variable_scope('discriminator', reuse=tf.AUTO_REUSE):
        with tf.variable_scope('conv1'):
            inputs = leaky_relu(conv2d('conv1', inputs, 64, 5, 2))
        with tf.variable_scope('conv2'):
            inputs = leaky_relu(instanceNorm('in1', conv2d('conv2', inputs, 128, 5, 2)))
        with tf.variable_scope('conv3'):
            inputs = leaky_relu(instanceNorm('in2', conv2d('conv3', inputs, 256, 5, 2)))
        with tf.variable_scope('conv4'):
            inputs = leaky_relu(instanceNorm('in3', conv2d('conv4', inputs, 512, 5, 2)))
        with tf.variable_scope('outputs'):
            inputs = conv2d('conv5', inputs, 1, 5, 1)
        return inputs
