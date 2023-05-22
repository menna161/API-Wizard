import tensorflow as tf
from contextlib import contextmanager
from tensorpack.tfutils.argscope import argscope
from tensorpack.tfutils.varreplace import remap_variables
from tensorpack.models import Conv2D, MaxPooling, GlobalAvgPooling, BatchNorm, FullyConnected, BNReLU, layer_register


def resnet_bottleneck(l, ch_out, stride, stride_first=False):
    shortcut = l
    norm_relu = (lambda x: tf.nn.relu(Norm(x)))
    l = Conv2D('conv1', l, ch_out, 1, strides=(stride if stride_first else 1), activation=norm_relu)
    '\n    Sec 5.1:\n    We use the ResNet-50 [16] variant from [12], noting that\n    the stride-2 convolutions are on 3×3 layers instead of on 1×1 layers\n    '
    l = Conv2D('conv2', l, ch_out, 3, strides=(1 if stride_first else stride), activation=norm_relu)
    "\n    Section 5.1:\n    For BN layers, the learnable scaling coefficient γ is initialized\n    to be 1, except for each residual block's last BN\n    where γ is initialized to be 0.\n    "
    l = Conv2D('conv3', l, (ch_out * 4), 1, activation=(lambda x: Norm(x, gamma_initializer=tf.zeros_initializer())))
    ret = (l + resnet_shortcut(shortcut, (ch_out * 4), stride, activation=(lambda x: Norm(x))))
    return tf.nn.relu(ret, name='block_output')
