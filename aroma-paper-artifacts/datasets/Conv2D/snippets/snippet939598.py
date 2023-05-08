import tensorflow as tf
import sys
import numpy as np
from tensorpack import *


def block_func(l, ch_out, stride):
    BN = (lambda x, name=None: BatchNorm('bn', x))
    shortcut = l
    l = Conv2D('conv1', l, ch_out, 1, strides=stride, activation=BNReLU)
    l = Conv2D('conv2', l, ch_out, 3, strides=1, activation=BNReLU)
    l = Conv2D('conv3', l, (ch_out * 4), 1, activation=BN)
    return tf.nn.relu((l + resnet_shortcut(shortcut, (ch_out * 4), stride, activation=BN)))
