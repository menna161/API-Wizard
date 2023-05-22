import tensorflow as tf
from contextlib import contextmanager
from tensorpack.tfutils.argscope import argscope
from tensorpack.tfutils.varreplace import remap_variables
from tensorpack.models import Conv2D, MaxPooling, GlobalAvgPooling, BatchNorm, FullyConnected, BNReLU, layer_register


def resnet_shortcut(l, n_out, stride, activation=tf.identity):
    n_in = l.get_shape().as_list()[1]
    if (n_in != n_out):
        return Conv2D('convshortcut', l, n_out, 1, strides=stride, activation=activation)
    else:
        return l
