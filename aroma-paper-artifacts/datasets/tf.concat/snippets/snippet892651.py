from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import copy
import tensorflow as tf
from collections import namedtuple
from tensorflow.python.util import nest


def _beam_search_step(time, func, state, batch_size, beam_size, alpha, pad_id, eos_id):
    print('st2', state)
    (seqs, log_probs) = state.inputs[:2]
    flat_seqs = _merge_first_two_dims(seqs)
    flat_state = nest.map_structure((lambda x: _merge_first_two_dims(x)), state.state)
    print('st3', flat_state)
    (step_log_probs, next_state) = func(flat_seqs, flat_state)
    step_log_probs = _split_first_two_dims(step_log_probs, batch_size, beam_size)
    print('st4', next_state)
    next_state = nest.map_structure((lambda x: _split_first_two_dims(x, batch_size, beam_size)), next_state)
    curr_log_probs = (tf.expand_dims(log_probs, 2) + step_log_probs)
    length_penalty = tf.pow(((5.0 + tf.to_float((time + 1))) / 6.0), alpha)
    curr_scores = (curr_log_probs / length_penalty)
    vocab_size = (curr_scores.shape[(- 1)].value or tf.shape(curr_scores)[(- 1)])
    curr_scores = tf.reshape(curr_scores, [(- 1), (beam_size * vocab_size)])
    (top_scores, top_indices) = tf.nn.top_k(curr_scores, k=(2 * beam_size))
    beam_indices = (top_indices // vocab_size)
    symbol_indices = (top_indices % vocab_size)
    candidate_seqs = _gather_2d(seqs, beam_indices)
    candidate_seqs = tf.concat([candidate_seqs, tf.expand_dims(symbol_indices, 2)], 2)
    flags = tf.equal(symbol_indices, eos_id)
    alive_scores = (top_scores + (tf.to_float(flags) * tf.float32.min))
    (alive_scores, alive_indices) = tf.nn.top_k(alive_scores, beam_size)
    alive_symbols = _gather_2d(symbol_indices, alive_indices)
    alive_indices = _gather_2d(beam_indices, alive_indices)
    alive_seqs = _gather_2d(seqs, alive_indices)
    alive_seqs = tf.concat([alive_seqs, tf.expand_dims(alive_symbols, 2)], 2)
    alive_state = nest.map_structure((lambda x: _gather_2d(x, alive_indices)), next_state)
    print('st5', alive_state)
    alive_log_probs = (alive_scores * length_penalty)
    (prev_fin_flags, prev_fin_seqs, prev_fin_scores) = state.finish
    step_fin_scores = (top_scores + ((1.0 - tf.to_float(flags)) * tf.float32.min))
    fin_flags = tf.concat([prev_fin_flags, flags], axis=1)
    fin_scores = tf.concat([prev_fin_scores, step_fin_scores], axis=1)
    (fin_scores, fin_indices) = tf.nn.top_k(fin_scores, beam_size)
    fin_flags = _gather_2d(fin_flags, fin_indices)
    pad_seqs = tf.fill([batch_size, beam_size, 1], tf.constant(pad_id, tf.int32))
    prev_fin_seqs = tf.concat([prev_fin_seqs, pad_seqs], axis=2)
    fin_seqs = tf.concat([prev_fin_seqs, candidate_seqs], axis=1)
    fin_seqs = _gather_2d(fin_seqs, fin_indices)
    new_state = BeamSearchState(inputs=(alive_seqs, alive_log_probs, alive_scores), state=alive_state, finish=(fin_flags, fin_seqs, fin_scores))
    return ((time + 1), new_state)
