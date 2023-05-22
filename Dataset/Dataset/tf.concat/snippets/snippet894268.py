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
    prenet_out = prenet(inputs, self._is_training, self.prenet_sizes, self.dropout_prob, scope='decoder_prenet')
    if (self._embed_to_concat is not None):
        concat_out = tf.concat([prenet_out, self._embed_to_concat], axis=(- 1), name='speaker_concat')
        return self._cell(concat_out, state)
    else:
        return self._cell(prenet_out, state)
