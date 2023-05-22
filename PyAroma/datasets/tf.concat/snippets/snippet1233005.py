import string
import numpy as np
import tensorflow as tf
from tensorflow.contrib.layers.python.layers import layers
from tensorflow.python.layers import base as base_layer
from tensorflow.python.framework import tensor_shape
from tensorflow.python.framework import dtypes
from tensorflow.python.ops import array_ops
from tensorflow.python.ops import init_ops
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import nn_ops
from tensorflow.python.ops import rnn_cell_impl
from tensorflow.contrib.rnn import LayerRNNCell, LayerNormBasicLSTMCell, BasicRNNCell
from tensorflow.python.ops import variable_scope as vs
from tensorflow.python.platform import tf_logging as logging
from tensorflow.python.util import nest
from nabu.neuralnetworks.components import ops
from nabu.neuralnetworks.components import rnn_cell_impl as rnn_cell_impl_extended
from ops import capsule_initializer
from ntm_ops import create_linear_initializer
import collections


def __call__(self, inputs, state, scope=None):
    'call wrapped cell with constant scope'
    (_, new_state) = self._cell(inputs, state, scope)
    output = tf.concat(nest.flatten(new_state), axis=1)
    return (output, new_state)
