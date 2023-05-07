import numpy as np
import tensorflow as tf
from tensorflow.contrib.rnn import RNNCell
from tensorflow.python.ops import rnn_cell_impl
from tensorflow.contrib.framework import nest
from tensorflow.contrib.seq2seq.python.ops.attention_wrapper import _bahdanau_score, _BaseAttentionMechanism, BahdanauAttention, AttentionWrapperState, AttentionMechanism, _BaseMonotonicAttentionMechanism, _maybe_mask_score, _prepare_memory, _monotonic_probability_fn
from tensorflow.python.layers.core import Dense
from .modules import prenet
import functools


def __init__(self, num_units, memory, memory_sequence_length=None, smoothing=False, cumulate_weights=True, name='LocationSensitiveAttention'):
    "Construct the Attention mechanism.\n        Args:\n                num_units: The depth of the query mechanism.\n                memory: The memory to query; usually the output of an RNN encoder.  This\n                        tensor should be shaped `[batch_size, max_time, ...]`.\n                memory_sequence_length (optional): Sequence lengths for the batch entries\n                        in memory.  If provided, the memory tensor rows are masked with zeros\n                        for values past the respective sequence lengths. Only relevant if mask_encoder = True.\n                smoothing (optional): Boolean. Determines which normalization function to use.\n                        Default normalization function (probablity_fn) is softmax. If smoothing is\n                        enabled, we replace softmax with:\n                                        a_{i, j} = sigmoid(e_{i, j}) / sum_j(sigmoid(e_{i, j}))\n                        Introduced in:\n                                J. K. Chorowski, D. Bahdanau, D. Serdyuk, K. Cho, and Y. Ben-\n                          gio, �쏛ttention-based models for speech recognition,�� in Ad-\n                          vances in Neural Information Processing Systems, 2015, pp.\n                          577��585.\n                        This is mainly used if the model wants to attend to multiple inputs parts\n                        at the same decoding step. We probably won't be using it since multiple sound\n                        frames may depend from the same character, probably not the way around.\n                        Note:\n                                We still keep it implemented in case we want to test it. They used it in the\n                                paper in the context of speech recognition, where one phoneme may depend on\n                                multiple subsequent sound frames.\n                name: Name to use when creating ops.\n        "
    normalization_function = (_smoothing_normalization if (smoothing == True) else None)
    super(LocationSensitiveAttention, self).__init__(num_units=num_units, memory=memory, memory_sequence_length=memory_sequence_length, probability_fn=normalization_function, name=name)
    self.location_convolution = tf.layers.Conv1D(filters=32, kernel_size=(31,), padding='same', use_bias=True, bias_initializer=tf.zeros_initializer(), name='location_features_convolution')
    self.location_layer = tf.layers.Dense(units=num_units, use_bias=False, dtype=tf.float32, name='location_features_layer')
    self._cumulate = cumulate_weights
