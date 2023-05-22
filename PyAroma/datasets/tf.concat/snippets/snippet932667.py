from __future__ import division
import tensorflow as tf
from ops import *
from utils import *


def generator_unet(image, options, reuse=False, name='generator'):
    dropout_rate = (0.5 if options.is_training else 1.0)
    with tf.variable_scope(name):
        if reuse:
            tf.get_variable_scope().reuse_variables()
        else:
            assert (tf.get_variable_scope().reuse is False)
        e1 = instance_norm(conv2d(image, options.gf_dim, name='g_e1_conv'))
        e2 = instance_norm(conv2d(lrelu(e1), (options.gf_dim * 2), name='g_e2_conv'), 'g_bn_e2')
        e3 = instance_norm(conv2d(lrelu(e2), (options.gf_dim * 4), s=3, name='g_e3_conv'), 'g_bn_e3')
        e4 = instance_norm(conv2d(lrelu(e3), (options.gf_dim * 8), s=[2, 1], name='g_e4_conv'), 'g_bn_e4')
        e5 = instance_norm(conv2d(lrelu(e4), (options.gf_dim * 8), s=[2, 1], name='g_e5_conv'), 'g_bn_e5')
        e6 = instance_norm(conv2d(lrelu(e5), (options.gf_dim * 8), s=[2, 7], name='g_e6_conv'), 'g_bn_e6')
        e7 = instance_norm(conv2d(lrelu(e6), (options.gf_dim * 8), s=[2, 1], name='g_e7_conv'), 'g_bn_e7')
        e8 = instance_norm(conv2d(lrelu(e7), (options.gf_dim * 8), s=[2, 1], name='g_e8_conv'), 'g_bn_e8')
        d1 = deconv2d(tf.nn.relu(e8), (options.gf_dim * 8), s=[2, 1], name='g_d1')
        d1 = tf.nn.dropout(d1, dropout_rate)
        d1 = tf.concat([instance_norm(d1, 'g_bn_d1'), e7], 3)
        d2 = deconv2d(tf.nn.relu(d1), (options.gf_dim * 8), s=[2, 1], name='g_d2')
        d2 = tf.nn.dropout(d2, dropout_rate)
        d2 = tf.concat([instance_norm(d2, 'g_bn_d2'), e6], 3)
        d3 = deconv2d(tf.nn.relu(d2), (options.gf_dim * 8), s=[2, 7], name='g_d3')
        d3 = tf.nn.dropout(d3, dropout_rate)
        d3 = tf.concat([instance_norm(d3, 'g_bn_d3'), e5], 3)
        d4 = deconv2d(tf.nn.relu(d3), (options.gf_dim * 8), s=[2, 1], name='g_d4')
        d4 = tf.concat([instance_norm(d4, 'g_bn_d4'), e4], 3)
        d5 = deconv2d(tf.nn.relu(d4), (options.gf_dim * 4), s=[2, 1], name='g_d5')
        d5 = tf.concat([instance_norm(d5, 'g_bn_d5'), e3], 3)
        d6 = deconv2d(tf.nn.relu(d5), (options.gf_dim * 2), s=3, name='g_d6')
        d6 = tf.concat([instance_norm(d6, 'g_bn_d6'), e2], 3)
        d7 = deconv2d(tf.nn.relu(d6), options.gf_dim, name='g_d7')
        d7 = tf.concat([instance_norm(d7, 'g_bn_d7'), e1], 3)
        d8 = deconv2d(tf.nn.relu(d7), options.output_c_dim, name='g_d8')
        return tf.nn.tanh(d8)
