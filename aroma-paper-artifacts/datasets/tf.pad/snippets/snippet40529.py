import tensorflow as tf
import tensorflow.contrib as tf_contrib
from utils import pytorch_xavier_weight_factor, pytorch_kaiming_weight_factor


def conv(x, channels, kernel=4, stride=2, pad=0, pad_type='zero', use_bias=True, bias_init=tf.constant_initializer(0.0), sn=False, scope='conv_0'):
    with tf.variable_scope(scope):
        if (pad > 0):
            h = x.get_shape().as_list()[1]
            if ((h % stride) == 0):
                pad = (pad * 2)
            else:
                pad = max((kernel - (h % stride)), 0)
            pad_top = (pad // 2)
            pad_bottom = (pad - pad_top)
            pad_left = (pad // 2)
            pad_right = (pad - pad_left)
            if (pad_type == 'zero'):
                x = tf.pad(x, [[0, 0], [pad_top, pad_bottom], [pad_left, pad_right], [0, 0]])
            if (pad_type == 'reflect'):
                x = tf.pad(x, [[0, 0], [pad_top, pad_bottom], [pad_left, pad_right], [0, 0]], mode='REFLECT')
        if sn:
            w = tf.get_variable('kernel', shape=[kernel, kernel, x.get_shape()[(- 1)], channels], initializer=weight_init, regularizer=weight_regularizer)
            x = tf.nn.conv2d(input=x, filter=spectral_norm(w), strides=[1, stride, stride, 1], padding='VALID')
            if use_bias:
                bias = tf.get_variable('bias', [channels], initializer=bias_init)
                x = tf.nn.bias_add(x, bias)
        else:
            x = tf.layers.conv2d(inputs=x, filters=channels, kernel_size=kernel, kernel_initializer=weight_init, kernel_regularizer=weight_regularizer, strides=stride, use_bias=use_bias, bias_initializer=bias_init)
        return x
