import numpy as np
import tensorflow as tf
from tensorflow.contrib.rnn import RNNCell
from tensorflow.python.ops import rnn_cell_impl
from tensorflow.contrib.framework import nest
from tensorflow.contrib.seq2seq.python.ops.attention_wrapper import _bahdanau_score, _BaseAttentionMechanism, BahdanauAttention, AttentionWrapperState, AttentionMechanism, _BaseMonotonicAttentionMechanism, _maybe_mask_score, _prepare_memory, _monotonic_probability_fn
from tensorflow.python.layers.core import Dense
from .modules import prenet
import functools


def call(self, inputs, state):
    (output, res_state) = self._cell(inputs, state)
    if (self._embed_to_concat is not None):
        tensors = [output, res_state.attention, self._embed_to_concat]
        return (tf.concat(tensors, axis=(- 1)), res_state)
    else:
        return (tf.concat([output, res_state.attention], axis=(- 1)), res_state)
