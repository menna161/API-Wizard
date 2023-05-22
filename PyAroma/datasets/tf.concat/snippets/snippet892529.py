from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import copy
import tensorflow as tf
import thumt.interface as interface
import thumt.layers as layers


def _encoder(cell_fw, cell_bw, inputs, sequence_length, dtype=None, scope=None):
    with tf.variable_scope((scope or 'encoder'), values=[inputs, sequence_length]):
        inputs_fw = inputs
        inputs_bw = tf.reverse_sequence(inputs, sequence_length, batch_axis=0, seq_axis=1)
        with tf.variable_scope('forward'):
            (output_fw, state_fw) = _gru_encoder(cell_fw, inputs_fw, sequence_length, None, dtype=dtype)
        with tf.variable_scope('backward'):
            (output_bw, state_bw) = _gru_encoder(cell_bw, inputs_bw, sequence_length, None, dtype=dtype)
            output_bw = tf.reverse_sequence(output_bw, sequence_length, batch_axis=0, seq_axis=1)
        results = {'annotation': tf.concat([output_fw, output_bw], axis=2), 'outputs': {'forward': output_fw, 'backward': output_bw}, 'final_states': {'forward': state_fw, 'backward': state_bw}}
        return results
