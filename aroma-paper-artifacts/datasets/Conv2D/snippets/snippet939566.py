import tensorflow as tf
from contextlib import contextmanager
from tensorpack.tfutils.argscope import argscope
from tensorpack.tfutils.varreplace import remap_variables
from tensorpack.models import Conv2D, MaxPooling, GlobalAvgPooling, BatchNorm, FullyConnected, BNReLU, layer_register


def resnet_backbone(image, num_blocks, group_func, block_func):
    '\n    Sec 5.1: We adopt the initialization of [15] for all convolutional layers.\n    TensorFlow does not have the true "MSRA init". We use variance_scaling as an approximation.\n    '
    with argscope(Conv2D, use_bias=False, kernel_initializer=tf.variance_scaling_initializer(scale=2.0, mode='fan_out')):
        l = Conv2D('conv0', image, 64, 7, strides=2, activation=BNReLU)
        l = MaxPooling('pool0', l, pool_size=3, strides=2, padding='SAME')
        l = group_func('group0', l, block_func, 64, num_blocks[0], 1)
        l = group_func('group1', l, block_func, 128, num_blocks[1], 2)
        l = group_func('group2', l, block_func, 256, num_blocks[2], 2)
        l = group_func('group3', l, block_func, 512, num_blocks[3], 2)
        l = GlobalAvgPooling('gap', l)
        logits = FullyConnected('linear', l, 1000, kernel_initializer=tf.random_normal_initializer(stddev=0.01))
    '\n    Sec 5.1:\n    The 1000-way fully-connected layer is initialized by\n    drawing weights from a zero-mean Gaussian with standard\n    deviation of 0.01.\n    '
    return logits
