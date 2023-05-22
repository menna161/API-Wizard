import sys
import argparse
import os
from contextlib import contextmanager, ExitStack
import tensorflow as tf
from tensorpack import *
from tensorpack.utils.gpu import get_nr_gpu
from tensorpack.tfutils.summary import *
from tensorpack.utils.argtools import log_once
from tensorpack.tfutils.collection import freeze_collection
from tensorpack.tfutils import get_current_tower_context
from tensorpack.tfutils.varreplace import custom_getter_scope
from tfbench.convnet_builder import ConvNetBuilder
from tfbench import model_config
from tensorpack.callbacks import ThroughputTracker


def _get_logits(self, image):

    def fp16_getter(getter, *args, **kwargs):
        name = (args[0] if len(args) else kwargs['name'])
        if ((not name.endswith('/W')) and (not name.endswith('/b'))):
            '\n                Following convention, convolution & fc are quantized.\n                BatchNorm (gamma & beta) are not quantized.\n                '
            return getter(*args, **kwargs)
        elif (kwargs['dtype'] == tf.float16):
            kwargs['dtype'] = tf.float32
            ret = getter(*args, **kwargs)
            ret = tf.cast(ret, tf.float16)
            log_once('Variable {} casted to fp16 ...'.format(name))
            return ret
        else:
            return getter(*args, **kwargs)

    def shortcut(l, n_in, n_out, stride):
        if (n_in != n_out):
            l = Conv2D('convshortcut', l, n_out, 1, strides=stride)
            l = BatchNorm('bnshortcut', l)
            return l
        else:
            return l

    def bottleneck(l, ch_out, stride, preact):
        ch_in = l.get_shape().as_list()[1]
        input = l
        l = Conv2D('conv1', l, ch_out, 1, strides=stride, activation=BNReLU)
        l = Conv2D('conv2', l, ch_out, 3, strides=1, activation=BNReLU)
        l = Conv2D('conv3', l, (ch_out * 4), 1, activation=tf.identity)
        l = BatchNorm('bn', l)
        ret = (l + shortcut(input, ch_in, (ch_out * 4), stride))
        return tf.nn.relu(ret)

    def layer(l, layername, block_func, features, count, stride, first=False):
        with tf.variable_scope(layername):
            with tf.variable_scope('block0'):
                l = block_func(l, features, stride, ('no_preact' if first else 'both_preact'))
            for i in range(1, count):
                with tf.variable_scope('block{}'.format(i)):
                    l = block_func(l, features, 1, 'default')
            return l
    defs = [3, 4, 6, 3]
    with ExitStack() as stack:
        stack.enter_context(argscope(Conv2D, use_bias=False, kernel_initializer=tf.variance_scaling_initializer(mode='fan_out')))
        stack.enter_context(argscope([Conv2D, MaxPooling, GlobalAvgPooling, BatchNorm], data_format=self.data_format))
        if args.use_fp16:
            stack.enter_context(custom_getter_scope(fp16_getter))
            image = tf.cast(image, tf.float16)
        logits = LinearWrap(image).Conv2D('conv0', 64, 7, strides=2).BatchNorm('bn0').tf.nn.relu().MaxPooling('pool0', 3, strides=2, padding='SAME').apply(layer, 'group0', bottleneck, 64, defs[0], 1, first=True).apply(layer, 'group1', bottleneck, 128, defs[1], 2).apply(layer, 'group2', bottleneck, 256, defs[2], 2).apply(layer, 'group3', bottleneck, 512, defs[3], 2).GlobalAvgPooling('gap').FullyConnected('linear', 1000)()
    if args.use_fp16:
        logits = tf.cast(logits, tf.float32)
    return logits
