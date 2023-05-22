import collections
import tensorflow as tf
from tensorflow.contrib.seq2seq.python.ops import decoder
from tensorflow.contrib.seq2seq.python.ops import helper as helper_py
from tensorflow.python.framework import dtypes
from tensorflow.python.framework import ops
from tensorflow.python.framework import tensor_shape
from tensorflow.python.layers import base as layers_base
from tensorflow.python.ops import rnn_cell_impl
from tensorflow.python.util import nest


def initialize(self, name=None):
    'Initialize the decoder.\n        Args:\n          name: Name scope for any created operations.\n        Returns:\n          `(finished, first_inputs, initial_state)`.\n        '
    return ((self._helper.initialize()[0], tf.concat([self._helper.initialize()[1], self._latent_vector], axis=(- 1))) + (self._initial_state,))
