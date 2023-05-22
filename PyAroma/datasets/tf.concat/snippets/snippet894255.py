import numpy as np
import tensorflow as tf
from tensorflow.contrib.rnn import RNNCell
from tensorflow.python.ops import rnn_cell_impl
from tensorflow.contrib.framework import nest
from tensorflow.contrib.seq2seq.python.ops.attention_wrapper import _bahdanau_score, _BaseAttentionMechanism, BahdanauAttention, AttentionWrapperState, AttentionMechanism, _BaseMonotonicAttentionMechanism, _maybe_mask_score, _prepare_memory, _monotonic_probability_fn
from tensorflow.python.layers.core import Dense
from .modules import prenet
import functools


def _compute_attention(attention_mechanism, cell_output, previous_alignments, attention_layer, is_manual_attention, manual_alignments, time):
    (computed_alignments, next_attention_state) = attention_mechanism(cell_output, state=previous_alignments)
    (batch_size, max_time) = (tf.shape(computed_alignments)[0], tf.shape(computed_alignments)[1])
    alignments = tf.cond(is_manual_attention, (lambda : manual_alignments[(:, time, :)]), (lambda : computed_alignments))
    expanded_alignments = tf.expand_dims(alignments, 1)
    context = tf.matmul(expanded_alignments, attention_mechanism.values)
    context = tf.squeeze(context, [1])
    if (attention_layer is not None):
        attention = attention_layer(tf.concat([cell_output, context], 1))
    else:
        attention = context
    return (attention, alignments, next_attention_state)
