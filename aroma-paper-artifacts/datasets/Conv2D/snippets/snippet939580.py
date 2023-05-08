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


def bottleneck(l, ch_out, stride, preact):
    ch_in = l.get_shape().as_list()[1]
    input = l
    l = Conv2D('conv1', l, ch_out, 1, strides=stride, activation=BNReLU)
    l = Conv2D('conv2', l, ch_out, 3, strides=1, activation=BNReLU)
    l = Conv2D('conv3', l, (ch_out * 4), 1, activation=tf.identity)
    l = BatchNorm('bn', l)
    ret = (l + shortcut(input, ch_in, (ch_out * 4), stride))
    return tf.nn.relu(ret)
