from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import copy
import tensorflow as tf
import thumt.interface as interface
import thumt.layers as layers
from tensorflow.contrib import rnn


def birnn(inputs, sequence_length, params):
    lstm_fw_cell = rnn.BasicLSTMCell(params.hidden_size)
    lstm_bw_cell = rnn.BasicLSTMCell(params.hidden_size)
    (outputs, states) = tf.nn.bidirectional_dynamic_rnn(lstm_fw_cell, lstm_bw_cell, inputs, sequence_length=sequence_length, dtype=tf.float32)
    (states_fw, states_bw) = outputs
    return tf.concat([states_fw, states_bw], axis=2)
