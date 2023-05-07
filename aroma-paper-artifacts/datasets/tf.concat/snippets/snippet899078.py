from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import abc
import functools
from os import path
import feature_map_constants as fmap_constants
import library_matching
import mass_spec_constants as ms_constants
import parse_sdf_utils
import plot_spectra_utils
import similarity as similarity_lib
import util
import numpy as np
import tensorflow as tf


def _make_learned_features(self, feature_dict, hparams, mode):
    sequence_length = feature_dict[fmap_constants.SMILES_TOKEN_LIST_LENGTH]
    embedding_table = tf.get_variable('atom_embeddings', [len(ms_constants.SMILES_TOKEN_NAMES), hparams.embedding_dim])
    processed_features = tf.nn.embedding_lookup(embedding_table, feature_dict[fmap_constants.SMILES])
    fw_rnn_cell = tf.nn.rnn_cell.LSTMCell(hparams.num_rnn_hidden_units)
    bw_rnn_cell = tf.nn.rnn_cell.LSTMCell(hparams.num_rnn_hidden_units)
    (rnn_outputs, _) = tf.nn.bidirectional_dynamic_rnn(fw_rnn_cell, bw_rnn_cell, processed_features, sequence_length=sequence_length, dtype=tf.float32)
    rnn_outputs = tf.concat(rnn_outputs, 2)
    if hparams.average_rnn_outputs:
        rnn_outputs = (tf.reduce_sum(rnn_outputs, axis=1) / tf.cast(sequence_length[(..., tf.newaxis)], tf.float32))
    else:
        rnn_outputs = rnn_outputs[(:, (- 1), ...)]
    return rnn_outputs
