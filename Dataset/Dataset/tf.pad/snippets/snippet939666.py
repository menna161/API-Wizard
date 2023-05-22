import numpy as np
from six.moves import xrange
import tensorflow as tf
from . import model as model_lib


def residual_block(cnn, depth, stride, pre_activation):
    'Residual block with identity short-cut.\n\n  Args:\n    cnn: the network to append residual blocks.\n    depth: the number of output filters for this residual block.\n    stride: Stride used in the first layer of the residual block.\n    pre_activation: use pre_activation structure or not.\n  '
    input_layer = cnn.top_layer
    in_size = cnn.top_size
    if (in_size != depth):
        shortcut = cnn.apool(1, 1, stride, stride, input_layer=input_layer, num_channels_in=in_size)
        padding = ((depth - in_size) // 2)
        if (cnn.channel_pos == 'channels_last'):
            shortcut = tf.pad(shortcut, [[0, 0], [0, 0], [0, 0], [padding, padding]])
        else:
            shortcut = tf.pad(shortcut, [[0, 0], [padding, padding], [0, 0], [0, 0]])
    else:
        shortcut = input_layer
    if pre_activation:
        res = cnn.batch_norm(input_layer)
        res = tf.nn.relu(res)
    else:
        res = input_layer
    cnn.conv(depth, 3, 3, stride, stride, input_layer=res, num_channels_in=in_size, use_batch_norm=True, bias=None)
    if pre_activation:
        res = cnn.conv(depth, 3, 3, 1, 1, activation=None, use_batch_norm=False, bias=None)
        output = (shortcut + res)
    else:
        res = cnn.conv(depth, 3, 3, 1, 1, activation=None, use_batch_norm=True, bias=None)
        output = tf.nn.relu((shortcut + res))
    cnn.top_layer = output
    cnn.top_size = depth
