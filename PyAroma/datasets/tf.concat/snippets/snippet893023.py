import logging
import numpy as np
import tensorflow as tf
import functions.tf_utils as tfu
import time
from tensorflow.contrib.memory_stats.python.ops.memory_stats_ops import BytesInUse


def network(images, bn_training, detailed_summary=False, use_keras=False):
    common = {'padding': 'valid', 'activation': 'ReLu', 'bn_training': bn_training, 'use_keras': use_keras}
    with tf.variable_scope('AdditiveNoise'):
        images = tf.cond(bn_training, (lambda : (images + tf.round(tf.random_normal(tf.shape(images), mean=tf.round(tf.random_normal([1], mean=0, stddev=2, dtype=tf.float32)), stddev=2, dtype=tf.float32)))), (lambda : images))
    margin_r1 = 31
    with tf.variable_scope('R1'):
        conv1_r1 = tfu.layers.conv3d(images, 16, [3, 3, 3], scope='conv1_R1', **common)
        crop_r1 = conv1_r1[(:, margin_r1:(- margin_r1), margin_r1:(- margin_r1), margin_r1:(- margin_r1), :)]
        conv2_r1 = tfu.layers.conv3d(crop_r1, 20, [3, 3, 3], scope='conv2_R1', **common)
        conv3_r1 = tfu.layers.conv3d(conv2_r1, 24, [3, 3, 3], scope='conv3_R1', **common)
        conv4_r1 = tfu.layers.conv3d(conv3_r1, 28, [3, 3, 3], scope='conv4_R1', **common)
        conv5_r1 = tfu.layers.conv3d(conv4_r1, 32, [3, 3, 3], scope='conv5_R1', **common)
        conv6_r1 = tfu.layers.conv3d(conv5_r1, 32, [3, 3, 3], scope='conv6_R1', **common)
        conv7_r1 = tfu.layers.conv3d(conv6_r1, 32, [3, 3, 3], scope='conv7_R1', **common)
    margin_r2 = 8
    margin_r2_up = 36
    with tf.variable_scope('R2'):
        images_r2 = tfu.layers.max_pooling3d(conv1_r1, pool_size=(2, 2, 2), strides=(2, 2, 2), padding='valid', scope='max_R2', use_keras=use_keras)
        conv1_r2 = tfu.layers.conv3d(images_r2, 30, [3, 3, 3], scope='conv1_R2', **common)
        crop_r2 = conv1_r2[(:, margin_r2:(- margin_r2), margin_r2:(- margin_r2), margin_r2:(- margin_r2), :)]
        conv2_r2 = tfu.layers.conv3d(crop_r2, 30, [3, 3, 3], scope='conv2_R2', **common)
        conv3_r2 = tfu.layers.conv3d(conv2_r2, 32, [3, 3, 3], dilation_rate=(2, 2, 2), scope='conv3_R2', **common)
        conv4_r2 = tfu.layers.conv3d(conv3_r2, 34, [3, 3, 3], dilation_rate=(2, 2, 2), scope='conv4_R2', **common)
        conv5_r2 = tfu.layers.conv3d(conv4_r2, 36, [3, 3, 3], dilation_rate=(2, 2, 2), scope='conv5_R2', **common)
        conv6_r2 = tfu.layers.conv3d(conv5_r2, 38, [3, 3, 3], dilation_rate=(2, 2, 2), scope='conv6_R2', **common)
        conv7_r2 = tfu.layers.upsampling3d(conv6_r2, scope='conv7_R2', interpolator='trilinear')
        concat_r2 = tf.concat([conv7_r2, conv1_r1[(:, margin_r2_up:(- margin_r2_up), margin_r2_up:(- margin_r2_up), margin_r2_up:(- margin_r2_up), :)]], axis=(- 1))
        conv8_r2 = tfu.layers.conv3d(concat_r2, 40, [3, 3, 3], scope='conv8_R2', **common)
    margin_r4_up1 = 1
    margin_r4_up2 = 36
    with tf.variable_scope('R4'):
        images_r4 = tfu.layers.max_pooling3d(conv1_r2, pool_size=(2, 2, 2), strides=(2, 2, 2), padding='valid', scope='max_R4', use_keras=use_keras)
        conv1_r4 = tfu.layers.conv3d(images_r4, 40, [3, 3, 3], scope='conv1_R4', **common)
        conv2_r4 = tfu.layers.conv3d(conv1_r4, 40, [3, 3, 3], scope='conv2_R4', **common)
        conv3_r4 = tfu.layers.conv3d(conv2_r4, 42, [3, 3, 3], dilation_rate=(2, 2, 2), scope='conv3_R4', **common)
        conv4_r4 = tfu.layers.conv3d(conv3_r4, 44, [3, 3, 3], dilation_rate=(2, 2, 2), scope='conv4_R4', **common)
        conv5_r4 = tfu.layers.conv3d(conv4_r4, 46, [3, 3, 3], dilation_rate=(2, 2, 2), scope='conv5_R4', **common)
        conv6_r4 = tfu.layers.upsampling3d(conv5_r4, scope='conv6_R4', interpolator='trilinear')
        concat1_r4 = tf.concat([conv6_r4, conv5_r2[(:, margin_r4_up1:(- margin_r4_up1), margin_r4_up1:(- margin_r4_up1), margin_r4_up1:(- margin_r4_up1), :)]], axis=(- 1))
        conv7_r4 = tfu.layers.conv3d(concat1_r4, 46, [3, 3, 3], scope='conv7_R4', **common)
        conv8_r4 = tfu.layers.upsampling3d(conv7_r4, scope='conv8_R4', interpolator='trilinear')
        concat2_r4 = tf.concat([conv8_r4, conv1_r1[(:, margin_r4_up2:(- margin_r4_up2), margin_r4_up2:(- margin_r4_up2), margin_r4_up2:(- margin_r4_up2), :)]], axis=(- 1))
        conv9_r4 = tfu.layers.conv3d(concat2_r4, 40, [3, 3, 3], scope='conv9_R4', **common)
    with tf.variable_scope('Merged'):
        conv_concat = tf.concat([conv7_r1, conv8_r2, conv9_r4], 4)
    with tf.variable_scope('FullyConnected'):
        conv7 = tfu.layers.conv3d(conv_concat, 120, [3, 3, 3], padding='valid', activation='ELu', bn_training=bn_training, scope='conv1_FC', use_keras=use_keras)
        conv8 = tfu.layers.conv3d(conv7, 50, [3, 3, 3], padding='valid', activation='ELu', bn_training=bn_training, scope='conv2_FC', use_keras=use_keras)
    with tf.variable_scope('DVF'):
        dvf_regnet = tfu.layers.conv3d(conv8, 3, [1, 1, 1], padding='valid', activation=None, bn_training=None, scope='DVF_RegNet', use_keras=use_keras)
    if detailed_summary:
        for i in range(1, 8):
            tensor_name = (('conv' + str(i)) + '_R1')
            tfu.summary.tensor2summary(eval(tensor_name.lower()), tensor_name, scope=('DetailedSummaryImages_R1_conv' + str(i)), selected_slices=1)
        for i in range(1, 9):
            tensor_name = (('conv' + str(i)) + '_R2')
            tfu.summary.tensor2summary(eval(tensor_name.lower()), tensor_name, scope=('DetailedSummaryImages_R2_conv' + str(i)), selected_slices=1)
        for i in range(1, 10):
            tensor_name = (('conv' + str(i)) + '_R4')
            tfu.summary.tensor2summary(eval(tensor_name.lower()), tensor_name, scope=('DetailedSummaryImages_R4_conv' + str(i)), selected_slices=1)
        tfu.summary.tensor2summary(conv7, 'conv7', scope='DetailedSummaryImages_conv7', selected_slices=1)
        tfu.summary.tensor2summary(conv8, 'conv8', scope='DetailedSummaryImages_conv8', selected_slices=1)
    return dvf_regnet
