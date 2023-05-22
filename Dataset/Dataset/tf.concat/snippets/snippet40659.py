import tensorflow as tf
from tensorflow.contrib.seq2seq import BahdanauAttention
from collections import namedtuple


def initial_state(self, batch_size, dtype):
    initial_alignments = self.initial_alignments(batch_size, dtype)
    initial_alpha = tf.concat([tf.ones([batch_size, 1], dtype=dtype), tf.zeros_like(initial_alignments, dtype=dtype)[(:, 1:)]], axis=1)
    initial_u = (0.5 * tf.ones([batch_size, 1], dtype=dtype))
    return ForwardAttentionState(initial_alignments, initial_alpha, initial_u)
