import tensorflow as tf
import sys
import numpy as np
from tensorpack import *


def build_graph(self, image, label):
    image = (image / 255.0)
    num_blocks = [3, 4, 6, 3]
    with argscope([Conv2D, MaxPooling, BatchNorm, GlobalAvgPooling], data_format='channels_first'), argscope(Conv2D, use_bias=False):
        logits = LinearWrap(image).tf.pad([[0, 0], [3, 3], [3, 3], [0, 0]]).Conv2D('conv0', 64, 7, strides=2, activation=BNReLU, padding='VALID').MaxPooling('pool0', 3, strides=2, padding='SAME').apply(group_func, 'group0', block_func, 64, num_blocks[0], 1).apply(group_func, 'group1', block_func, 128, num_blocks[1], 2).apply(group_func, 'group2', block_func, 256, num_blocks[2], 2).apply(group_func, 'group3', block_func, 512, num_blocks[3], 2).GlobalAvgPooling('gap').FullyConnected('linear', 1000, activation=tf.identity)()
    cost = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=label)
    cost = tf.reduce_mean(cost, name='cost')
    return cost
