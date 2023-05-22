import tensorflow as tf
from tensorflow.contrib.seq2seq import BahdanauAttention
from collections import namedtuple


def __call__(self, query, state):
    (previous_alignments, prev_alpha, prev_u) = state
    with tf.variable_scope(None, 'location_sensitive_attention', [query]):
        processed_query = (self.query_layer(query) if self.query_layer else query)
        expanded_processed_query = tf.expand_dims(processed_query, 1)
        expanded_alignments = tf.expand_dims(previous_alignments, axis=2)
        f = self.location_convolution(expanded_alignments)
        processed_location_features = self.location_layer(f)
        energy = _location_sensitive_score(expanded_processed_query, processed_location_features, self.keys)
    alignments = self._probability_fn(energy, state)
    prev_alpha_n_minus_1 = tf.pad(prev_alpha[(:, :(- 1))], paddings=[[0, 0], [1, 0]])
    alpha = (((((1 - prev_u) * prev_alpha) + (prev_u * prev_alpha_n_minus_1)) + 1e-07) * alignments)
    alpha_normalized = (alpha / tf.reduce_sum(alpha, axis=1, keep_dims=True))
    if self._use_transition_agent:
        context = _calculate_context(alpha_normalized, self.values)
        transition_factor_input = tf.concat([context, processed_query], axis=(- 1))
        transition_factor = self.transition_factor_projection(transition_factor_input)
    else:
        transition_factor = prev_u
    if self._cumulative_weights:
        next_state = ForwardAttentionState((alignments + previous_alignments), alpha_normalized, transition_factor)
    else:
        next_state = ForwardAttentionState(alignments, alpha_normalized, transition_factor)
    return (alpha_normalized, next_state)
