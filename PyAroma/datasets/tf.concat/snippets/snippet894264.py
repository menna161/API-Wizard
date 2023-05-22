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
    "Perform a step of attention-wrapped RNN.\n        - Step 1: Mix the `inputs` and previous step's `attention` output via\n          `cell_input_fn`.\n        - Step 2: Call the wrapped `cell` with this input and its previous state.\n        - Step 3: Score the cell's output with `attention_mechanism`.\n        - Step 4: Calculate the alignments by passing the score through the\n          `normalizer`.\n        - Step 5: Calculate the context vector as the inner product between the\n          alignments and the attention_mechanism's values (memory).\n        - Step 6: Calculate the attention output by concatenating the cell output\n          and context through the attention layer (a linear layer with\n          `attention_layer_size` outputs).\n        Args:\n          inputs: (Possibly nested tuple of) Tensor, the input at this time step.\n          state: An instance of `AttentionWrapperState` containing\n            tensors from the previous time step.\n        Returns:\n          A tuple `(attention_or_cell_output, next_state)`, where:\n          - `attention_or_cell_output` depending on `output_attention`.\n          - `next_state` is an instance of `AttentionWrapperState`\n             containing the state calculated at this time step.\n        Raises:\n          TypeError: If `state` is not an instance of `AttentionWrapperState`.\n        "
    if (not isinstance(state, AttentionWrapperState)):
        raise TypeError(('Expected state to be instance of AttentionWrapperState. Received type %s instead.' % type(state)))
    cell_inputs = self._cell_input_fn(inputs, state.attention)
    cell_state = state.cell_state
    (cell_output, next_cell_state) = self._cell(cell_inputs, cell_state)
    cell_batch_size = (cell_output.shape[0].value or tf.shape(cell_output)[0])
    error_message = (('When applying AttentionWrapper %s: ' % self.name) + 'Non-matching batch sizes between the memory (encoder output) and the query (decoder output).  Are you using the BeamSearchDecoder?  You may need to tile your memory input via the tf.contrib.seq2seq.tile_batch function with argument multiple=beam_width.')
    with tf.control_dependencies(self._batch_size_checks(cell_batch_size, error_message)):
        cell_output = tf.identity(cell_output, name='checked_cell_output')
    if self._is_multi:
        previous_attention_state = state.attention_state
        previous_alignment_history = state.alignment_history
    else:
        previous_attention_state = [state.attention_state]
        previous_alignment_history = [state.alignment_history]
    all_alignments = []
    all_attentions = []
    all_attention_states = []
    maybe_all_histories = []
    for (i, attention_mechanism) in enumerate(self._attention_mechanisms):
        (attention, alignments, next_attention_state) = _compute_attention(attention_mechanism, cell_output, previous_attention_state[i], (self._attention_layers[i] if self._attention_layers else None), self.is_manual_attention, self.manual_alignments, state.time)
        alignment_history = (previous_alignment_history[i].write(state.time, alignments) if self._alignment_history else ())
        all_attention_states.append(next_attention_state)
        all_alignments.append(alignments)
        all_attentions.append(attention)
        maybe_all_histories.append(alignment_history)
    attention = tf.concat(all_attentions, 1)
    next_state = AttentionWrapperState(time=(state.time + 1), cell_state=next_cell_state, attention=attention, attention_state=self._item_or_tuple(all_attention_states), alignments=self._item_or_tuple(all_alignments), alignment_history=self._item_or_tuple(maybe_all_histories))
    if self._output_attention:
        return (attention, next_state)
    else:
        return (cell_output, next_state)
