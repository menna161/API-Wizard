import tensorflow as tf
import numpy as np
import os
from PIL import Image
import scipy.misc as misc


def generator(self, inputs_condition):
    inputs = inputs_condition
    with tf.variable_scope('generator'):
        inputs1 = leaky_relu(conv2d('conv1', inputs, 64, 5, 2))
        inputs2 = leaky_relu(instanceNorm('in1', conv2d('conv2', inputs1, 128, 5, 2)))
        inputs3 = leaky_relu(instanceNorm('in2', conv2d('conv3', inputs2, 256, 5, 2)))
        inputs4 = leaky_relu(instanceNorm('in3', conv2d('conv4', inputs3, 512, 5, 2)))
        inputs5 = leaky_relu(instanceNorm('in4', conv2d('conv5', inputs4, 512, 5, 2)))
        inputs6 = leaky_relu(instanceNorm('in5', conv2d('conv6', inputs5, 512, 5, 2)))
        inputs7 = leaky_relu(instanceNorm('in6', conv2d('conv7', inputs6, 512, 5, 2)))
        inputs8 = leaky_relu(instanceNorm('in7', conv2d('conv8', inputs7, 512, 5, 2)))
        outputs1 = tf.nn.relu(tf.concat([tf.nn.dropout(instanceNorm('in9', deconv2d('dconv1', inputs8, 512, 5, 2)), 0.5), inputs7], axis=3))
        outputs2 = tf.nn.relu(tf.concat([tf.nn.dropout(instanceNorm('in10', deconv2d('dconv2', outputs1, 512, 5, 2)), 0.5), inputs6], axis=3))
        outputs3 = tf.nn.relu(tf.concat([tf.nn.dropout(instanceNorm('in11', deconv2d('dconv3', outputs2, 512, 5, 2)), 0.5), inputs5], axis=3))
        outputs4 = tf.nn.relu(tf.concat([instanceNorm('in12', deconv2d('dconv4', outputs3, 512, 5, 2)), inputs4], axis=3))
        outputs5 = tf.nn.relu(tf.concat([instanceNorm('in13', deconv2d('dconv5', outputs4, 256, 5, 2)), inputs3], axis=3))
        outputs6 = tf.nn.relu(tf.concat([instanceNorm('in14', deconv2d('dconv6', outputs5, 128, 5, 2)), inputs2], axis=3))
        outputs7 = tf.nn.relu(tf.concat([instanceNorm('in15', deconv2d('dconv7', outputs6, 64, 5, 2)), inputs1], axis=3))
        outputs8 = tf.nn.tanh(deconv2d('dconv8', outputs7, 3, 5, 2))
        return outputs8
