import argparse
import numpy as np
import os
import multiprocessing as mp
import tensorflow as tf
from tensorpack import *
from tensorpack.utils import logger
from tensorpack.tfutils.tower import TowerFunc
from tensorpack.tfutils.varreplace import custom_getter_scope
from tensorpack.dataflow import dataset


def build_graph(image, label):
    if USE_FP16:
        image = tf.cast(image, tf.float16)

    def activation(x):
        return tf.nn.leaky_relu(x, alpha=0.1)

    def residual(name, x, chan):
        with tf.variable_scope(name):
            x = Conv2D('res1', x, chan, 3)
            x = BatchNorm('bn1', x)
            x = activation(x)
            x = Conv2D('res2', x, chan, 3)
            x = BatchNorm('bn2', x)
            x = activation(x)
            return x

    def fp16_getter(getter, *args, **kwargs):
        name = (args[0] if len(args) else kwargs['name'])
        if ((not USE_FP16) or ((not name.endswith('/W')) and (not name.endswith('/b')))):
            return getter(*args, **kwargs)
        elif (kwargs['dtype'] == tf.float16):
            kwargs['dtype'] = tf.float32
            ret = getter(*args, **kwargs)
            return tf.cast(ret, tf.float16)
        else:
            return getter(*args, **kwargs)
    with custom_getter_scope(fp16_getter), argscope(Conv2D, activation=tf.identity, use_bias=False), argscope([Conv2D, MaxPooling, BatchNorm], data_format=DATA_FORMAT), argscope(BatchNorm, momentum=0.8):
        with tf.variable_scope('prep'):
            l = Conv2D('conv', image, 64, 3)
            l = BatchNorm('bn', l)
            l = activation(l)
        with tf.variable_scope('layer1'):
            l = Conv2D('conv', l, 128, 3)
            l = MaxPooling('pool', l, 2)
            l = BatchNorm('bn', l)
            l = activation(l)
            l = (l + residual('res', l, 128))
        with tf.variable_scope('layer2'):
            l = Conv2D('conv', l, 256, 3)
            l = MaxPooling('pool', l, 2)
            l = BatchNorm('bn', l)
            l = activation(l)
        with tf.variable_scope('layer3'):
            l = Conv2D('conv', l, 512, 3)
            l = MaxPooling('pool', l, 2)
            l = BatchNorm('bn', l)
            l = activation(l)
            l = (l + residual('res', l, 512))
        l = tf.reduce_max(l, axis=([2, 3] if (DATA_FORMAT == 'NCHW') else [1, 2]))
        l = FullyConnected('fc', l, 10, use_bias=False)
        logits = tf.cast((l * 0.125), tf.float32, name='logits')
    cost = tf.nn.softmax_cross_entropy_with_logits(labels=label, logits=logits)
    cost = tf.reduce_sum(cost)
    wd_cost = regularize_cost('.*', l2_regularizer((0.0005 * BATCH)), name='regularize_loss')
    correct = tf.equal(tf.argmax(logits, axis=1), tf.argmax(label, axis=1), name='correct')
    return tf.add_n([cost, wd_cost], name='cost')
