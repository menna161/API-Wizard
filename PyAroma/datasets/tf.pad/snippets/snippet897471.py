import tensorflow as tf
import vgg
from tensorflow.python.ops import control_flow_ops
import tensorflow.contrib.slim as slim
import cv2


def conv(x, channels, kernel=3, stride=1, pad=1, pad_type='zero', scope='conv_0'):
    with tf.variable_scope(scope):
        if (pad_type == 'zero'):
            x = tf.pad(x, [[0, 0], [pad, pad], [pad, pad], [0, 0]])
        if (pad_type == 'reflect'):
            x = tf.pad(x, [[0, 0], [pad, pad], [pad, pad], [0, 0]], mode='REFLECT')
        x = tf.layers.conv2d(x, channels, kernel, stride, kernel_initializer=tf.contrib.layers.xavier_initializer())
        return x
