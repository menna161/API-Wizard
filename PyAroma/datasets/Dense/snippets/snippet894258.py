import numpy as np
import tensorflow as tf
from tensorflow.contrib.rnn import RNNCell
from tensorflow.python.ops import rnn_cell_impl
from tensorflow.contrib.framework import nest
from tensorflow.contrib.seq2seq.python.ops.attention_wrapper import _bahdanau_score, _BaseAttentionMechanism, BahdanauAttention, AttentionWrapperState, AttentionMechanism, _BaseMonotonicAttentionMechanism, _maybe_mask_score, _prepare_memory, _monotonic_probability_fn
from tensorflow.python.layers.core import Dense
from .modules import prenet
import functools


def __init__(self, cell, attention_mechanism, is_manual_attention, manual_alignments, attention_layer_size=None, alignment_history=False, cell_input_fn=None, output_attention=True, initial_cell_state=None, name=None):
    'Construct the `AttentionWrapper`.\n        **NOTE** If you are using the `BeamSearchDecoder` with a cell wrapped in\n        `AttentionWrapper`, then you must ensure that:\n        - The encoder output has been tiled to `beam_width` via\n          @{tf.contrib.seq2seq.tile_batch} (NOT `tf.tile`).\n        - The `batch_size` argument passed to the `zero_state` method of this\n          wrapper is equal to `true_batch_size * beam_width`.\n        - The initial state created with `zero_state` above contains a\n          `cell_state` value containing properly tiled final state from the\n          encoder.\n        An example:\n        ```\n        tiled_encoder_outputs = tf.contrib.seq2seq.tile_batch(\n            encoder_outputs, multiplier=beam_width)\n        tiled_encoder_final_state = tf.conrib.seq2seq.tile_batch(\n            encoder_final_state, multiplier=beam_width)\n        tiled_sequence_length = tf.contrib.seq2seq.tile_batch(\n            sequence_length, multiplier=beam_width)\n        attention_mechanism = MyFavoriteAttentionMechanism(\n            num_units=attention_depth,\n            memory=tiled_inputs,\n            memory_sequence_length=tiled_sequence_length)\n        attention_cell = AttentionWrapper(cell, attention_mechanism, ...)\n        decoder_initial_state = attention_cell.zero_state(\n            dtype, batch_size=true_batch_size * beam_width)\n        decoder_initial_state = decoder_initial_state.clone(\n            cell_state=tiled_encoder_final_state)\n        ```\n        Args:\n          cell: An instance of `RNNCell`.\n          attention_mechanism: A list of `AttentionMechanism` instances or a single\n            instance.\n          attention_layer_size: A list of Python integers or a single Python\n            integer, the depth of the attention (output) layer(s). If None\n            (default), use the context as attention at each time step. Otherwise,\n            feed the context and cell output into the attention layer to generate\n            attention at each time step. If attention_mechanism is a list,\n            attention_layer_size must be a list of the same length.\n          alignment_history: Python boolean, whether to store alignment history\n            from all time steps in the final output state (currently stored as a\n            time major `TensorArray` on which you must call `stack()`).\n          cell_input_fn: (optional) A `callable`.  The default is:\n            `lambda inputs, attention: tf.concat([inputs, attention], -1)`.\n          output_attention: Python bool.  If `True` (default), the output at each\n            time step is the attention value.  This is the behavior of Luong-style\n            attention mechanisms.  If `False`, the output at each time step is\n            the output of `cell`.  This is the behavior of Bhadanau-style\n            attention mechanisms.  In both cases, the `attention` tensor is\n            propagated to the next time step via the state and is used there.\n            This flag only controls whether the attention mechanism is propagated\n            up to the next cell in an RNN stack or to the top RNN output.\n          initial_cell_state: The initial state value to use for the cell when\n            the user calls `zero_state()`.  Note that if this value is provided\n            now, and the user uses a `batch_size` argument of `zero_state` which\n            does not match the batch size of `initial_cell_state`, proper\n            behavior is not guaranteed.\n          name: Name to use when creating ops.\n        Raises:\n          TypeError: `attention_layer_size` is not None and (`attention_mechanism`\n            is a list but `attention_layer_size` is not; or vice versa).\n          ValueError: if `attention_layer_size` is not None, `attention_mechanism`\n            is a list, and its length does not match that of `attention_layer_size`.\n        '
    super(AttentionWrapper, self).__init__(name=name)
    self.is_manual_attention = is_manual_attention
    self.manual_alignments = manual_alignments
    rnn_cell_impl.assert_like_rnncell('cell', cell)
    if isinstance(attention_mechanism, (list, tuple)):
        self._is_multi = True
        attention_mechanisms = attention_mechanism
        for attention_mechanism in attention_mechanisms:
            if (not isinstance(attention_mechanism, AttentionMechanism)):
                raise TypeError(('attention_mechanism must contain only instances of AttentionMechanism, saw type: %s' % type(attention_mechanism).__name__))
    else:
        self._is_multi = False
        if (not isinstance(attention_mechanism, AttentionMechanism)):
            raise TypeError(('attention_mechanism must be an AttentionMechanism or list of multiple AttentionMechanism instances, saw type: %s' % type(attention_mechanism).__name__))
        attention_mechanisms = (attention_mechanism,)
    if (cell_input_fn is None):
        cell_input_fn = (lambda inputs, attention: tf.concat([inputs, attention], (- 1)))
    elif (not callable(cell_input_fn)):
        raise TypeError(('cell_input_fn must be callable, saw type: %s' % type(cell_input_fn).__name__))
    if (attention_layer_size is not None):
        attention_layer_sizes = tuple((attention_layer_size if isinstance(attention_layer_size, (list, tuple)) else (attention_layer_size,)))
        if (len(attention_layer_sizes) != len(attention_mechanisms)):
            raise ValueError(('If provided, attention_layer_size must contain exactly one integer per attention_mechanism, saw: %d vs %d' % (len(attention_layer_sizes), len(attention_mechanisms))))
        self._attention_layers = tuple((layers_core.Dense(attention_layer_size, name='attention_layer', use_bias=False, dtype=attention_mechanisms[i].dtype) for (i, attention_layer_size) in enumerate(attention_layer_sizes)))
        self._attention_layer_size = sum(attention_layer_sizes)
    else:
        self._attention_layers = None
        self._attention_layer_size = sum((attention_mechanism.values.get_shape()[(- 1)].value for attention_mechanism in attention_mechanisms))
    self._cell = cell
    self._attention_mechanisms = attention_mechanisms
    self._cell_input_fn = cell_input_fn
    self._output_attention = output_attention
    self._alignment_history = alignment_history
    with tf.name_scope(name, 'AttentionWrapperInit'):
        if (initial_cell_state is None):
            self._initial_cell_state = None
        else:
            final_state_tensor = nest.flatten(initial_cell_state)[(- 1)]
            state_batch_size = (final_state_tensor.shape[0].value or tf.shape(final_state_tensor)[0])
            error_message = (('When constructing AttentionWrapper %s: ' % self._base_name) + 'Non-matching batch sizes between the memory (encoder output) and initial_cell_state.  Are you using the BeamSearchDecoder?  You may need to tile your initial state via the tf.contrib.seq2seq.tile_batch function with argument multiple=beam_width.')
            with tf.control_dependencies(self._batch_size_checks(state_batch_size, error_message)):
                self._initial_cell_state = nest.map_structure((lambda s: tf.identity(s, name='check_initial_cell_state')), initial_cell_state)
