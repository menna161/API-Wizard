import tensorflow as tf
import sys
import numpy as np
from tensorpack import *


def resnet_shortcut(l, n_out, stride, activation=tf.identity):
    n_in = l.get_shape().as_list()[1]
    if (n_in != n_out):
        return Conv2D('convshortcut', l, n_out, 1, strides=stride, activation=activation)
    else:
        return l
