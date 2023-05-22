import tensorflow as tf
import numpy as np
import functions.tf_utils as tfu
import logging
import time
from tensorflow.contrib.memory_stats.python.ops.memory_stats_ops import BytesInUse


def network(images, bn_training, detailed_summary=False, use_keras=False):
    with tf.variable_scope('AdditiveNoise'):
        images = tf.cond(bn_training, (lambda : (images + tf.round(tf.random_normal(tf.shape(images), mean=tf.round(tf.random_normal([1], mean=0, stddev=2, dtype=tf.float32)), stddev=2, dtype=tf.float32)))), (lambda : images))
    common = {'padding': 'valid', 'activation': 'ReLu', 'bn_training': bn_training, 'use_keras': use_keras}
    with tf.variable_scope('R1'):
        conv1_r1 = tfu.layers.conv3d(images, 12, [3, 3, 3], scope='conv1_R1', padding='same', activation='ReLu', bn_training=bn_training, use_keras=use_keras)
    with tf.variable_scope('R2'):
        images_r2 = tfu.layers.max_pooling3d(conv1_r1, pool_size=(2, 2, 2), strides=(2, 2, 2), padding='same', scope='max_R2', use_keras=use_keras)
        conv1_r2 = tfu.layers.conv3d(images_r2, 24, [3, 3, 3], scope='conv1_R2', **common)
    with tf.variable_scope('R3'):
        images_r3 = tfu.layers.max_pooling3d(conv1_r2, pool_size=(2, 2, 2), strides=(2, 2, 2), padding='same', scope='max_R3', use_keras=use_keras)
        conv1_r3 = tfu.layers.conv3d(images_r3, 28, [3, 3, 3], scope='conv1_R3', **common)
    with tf.variable_scope('R4'):
        images_r4 = tfu.layers.max_pooling3d(conv1_r3, pool_size=(2, 2, 2), strides=(2, 2, 2), padding='valid', scope='max_R4', use_keras=use_keras)
        conv1_r4 = tfu.layers.conv3d(images_r4, 32, [3, 3, 3], scope='conv1_R4', padding='same', activation='ReLu', bn_training=bn_training, use_keras=use_keras)
        conv2_r4 = tfu.layers.conv3d(conv1_r4, 40, [3, 3, 3], scope='conv2_R4', padding='same', activation='ReLu', bn_training=bn_training, use_keras=use_keras)
        conv3_r4 = tfu.layers.conv3d(conv2_r4, 44, [3, 3, 3], scope='conv3_R4', padding='same', activation='ReLu', bn_training=bn_training, use_keras=use_keras)
    with tf.variable_scope('R3_Up'):
        conv1_r3_up = tfu.layers.upsampling3d(conv3_r4, scope='conv1_R3_Up', interpolator='trilinear')
        concat_r3_up = tf.concat([conv1_r3_up, conv1_r3], 4)
        conv2_r3 = tfu.layers.conv3d(concat_r3_up, 32, [3, 3, 3], scope='conv2_R3_Up', padding='same', activation='ReLu', bn_training=bn_training, use_keras=use_keras)
    with tf.variable_scope('R2_Up'):
        conv1_r2_up = tfu.layers.upsampling3d(conv2_r3, scope='conv1_R2_Up', interpolator='trilinear')
        mr = 1
        concat_r2_up = tf.concat([tf.pad(conv1_r2_up, ([0, 0], [mr, mr], [mr, mr], [mr, mr], [0, 0]), constant_values=0), conv1_r2], 4)
        conv2_r2 = tfu.layers.conv3d(concat_r2_up, 18, [3, 3, 3], scope='conv2_R2_Up', padding='same', activation='ReLu', bn_training=bn_training, use_keras=use_keras)
    with tf.variable_scope('R1_Up'):
        conv1_r1_up = tfu.layers.upsampling3d(conv2_r2, scope='conv1_R1_Up', interpolator='trilinear')
        mr = 1
        concat_r1_up = tf.concat([tf.pad(conv1_r1_up, ([0, 0], [mr, mr], [mr, mr], [mr, mr], [0, 0]), constant_values=0), conv1_r1], 4)
        conv2_r1 = tfu.layers.conv3d(concat_r1_up, 12, [3, 3, 3], scope='conv1_R2_Up', padding='same', activation='ReLu', bn_training=bn_training, use_keras=use_keras)
    with tf.variable_scope('DVF'):
        dvf_regnet = tfu.layers.conv3d(conv2_r1, 3, [1, 1, 1], padding='valid', activation=None, bn_training=None, scope='DVF_RegNet')
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
    return dvf_regnet
