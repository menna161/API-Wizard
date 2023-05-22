import numpy as np
import tensorflow as tf
from tensorflow.contrib.rnn import RNNCell
from tensorflow.python.ops import rnn_cell_impl
from tensorflow.contrib.framework import nest
from tensorflow.contrib.seq2seq.python.ops.attention_wrapper import _bahdanau_score, _BaseAttentionMechanism, BahdanauAttention, AttentionWrapperState, AttentionMechanism, _BaseMonotonicAttentionMechanism, _maybe_mask_score, _prepare_memory, _monotonic_probability_fn
from tensorflow.python.layers.core import Dense
from .modules import prenet
import functools


def __init__(self, num_mixtures, memory, memory_sequence_length=None, check_inner_dims_defined=True, score_mask_value=None, name='GmmAttention'):
    self.dtype = memory.dtype
    self.num_mixtures = num_mixtures
    self.query_layer = tf.layers.Dense((3 * num_mixtures), name='gmm_query_layer', use_bias=True, dtype=self.dtype)
    with tf.name_scope(name, 'GmmAttentionMechanismInit'):
        if (score_mask_value is None):
            score_mask_value = 0.0
        self._maybe_mask_score = functools.partial(_maybe_mask_score, memory_sequence_length=memory_sequence_length, score_mask_value=score_mask_value)
        self._value = _prepare_memory(memory, memory_sequence_length, check_inner_dims_defined)
        self._batch_size = (self._value.shape[0].value or tf.shape(self._value)[0])
        self._alignments_size = (self._value.shape[1].value or tf.shape(self._value)[1])
