import numpy as np
import tensorflow as tf
from tensorflow.contrib.rnn import RNNCell
from tensorflow.python.ops import rnn_cell_impl
from tensorflow.contrib.framework import nest
from tensorflow.contrib.seq2seq.python.ops.attention_wrapper import _bahdanau_score, _BaseAttentionMechanism, BahdanauAttention, AttentionWrapperState, AttentionMechanism, _BaseMonotonicAttentionMechanism, _maybe_mask_score, _prepare_memory, _monotonic_probability_fn
from tensorflow.python.layers.core import Dense
from .modules import prenet
import functools


def __init__(self, num_units, memory, memory_sequence_length=None, normalize=False, score_mask_value=None, sigmoid_noise=0.0, sigmoid_noise_seed=None, score_bias_init=0.0, mode='parallel', dtype=None, name='BahdanauMonotonicAttentionHccho'):
    "Construct the Attention mechanism.\n\n        Args:\n          num_units: The depth of the query mechanism.\n          memory: The memory to query; usually the output of an RNN encoder.  This\n            tensor should be shaped `[batch_size, max_time, ...]`.\n          memory_sequence_length (optional): Sequence lengths for the batch entries\n            in memory.  If provided, the memory tensor rows are masked with zeros\n            for values past the respective sequence lengths.\n          normalize: Python boolean.  Whether to normalize the energy term.\n          score_mask_value: (optional): The mask value for score before passing into\n            `probability_fn`. The default is -inf. Only used if\n            `memory_sequence_length` is not None.\n          sigmoid_noise: Standard deviation of pre-sigmoid noise.  See the docstring\n            for `_monotonic_probability_fn` for more information.\n          sigmoid_noise_seed: (optional) Random seed for pre-sigmoid noise.\n          score_bias_init: Initial value for score bias scalar.  It's recommended to\n            initialize this to a negative value when the length of the memory is\n            large.\n          mode: How to compute the attention distribution.  Must be one of\n            'recursive', 'parallel', or 'hard'.  See the docstring for\n            `tf.contrib.seq2seq.monotonic_attention` for more information.\n          dtype: The data type for the query and memory layers of the attention\n            mechanism.\n          name: Name to use when creating ops.\n        "
    if (dtype is None):
        dtype = tf.float32
    wrapped_probability_fn = functools.partial(_monotonic_probability_fn, sigmoid_noise=sigmoid_noise, mode=mode, seed=sigmoid_noise_seed)
    super(BahdanauMonotonicAttention_hccho, self).__init__(query_layer=Dense(num_units, name='query_layer', use_bias=False, dtype=dtype), memory_layer=Dense(num_units, name='memory_layer', use_bias=False, dtype=dtype), memory=memory, probability_fn=wrapped_probability_fn, memory_sequence_length=memory_sequence_length, score_mask_value=score_mask_value, name=name)
    self._num_units = num_units
    self._normalize = normalize
    self._name = name
    self._score_bias_init = score_bias_init
