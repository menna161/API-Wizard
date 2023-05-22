import string
import tensorflow as tf
from tensorflow.python.ops.rnn import bidirectional_dynamic_rnn, dynamic_rnn
from nabu.neuralnetworks.components import ops, rnn_cell, rnn, rnn_cell_impl
from ops import capsule_initializer
from tensorflow.python.ops import gen_nn_ops
from tensorflow.python.framework import ops


def __call__(self, inputs, sequence_length, scope=None):
    '\n\t\tCreate the variables and do the forward computation\n\n\t\tArgs:\n\t\t\tinputs: the input to the layer as a\n\t\t\t\t[batch_size, max_length, dim] tensor\n\t\t\tsequence_length: the length of the input sequences as a\n\t\t\t\t[batch_size] tensor\n\t\t\tscope: The variable scope sets the namespace under which\n\t\t\t\tthe variables created during this call will be stored.\n\n\t\tReturns:\n\t\t\tthe output of the layer\n\t\t'
    with tf.variable_scope((scope or type(self).__name__)):
        if self.linear_out_flag:
            lstm_cell_type = rnn_cell.LayerNormBasicLSTMCellLineairOut
        else:
            lstm_cell_type = tf.contrib.rnn.LayerNormBasicLSTMCell
        lstm_cell_fw = lstm_cell_type(num_units=self.num_units, activation=self.activation_fn, layer_norm=self.layer_norm, dropout_keep_prob=self.recurrent_dropout, reuse=tf.get_variable_scope().reuse)
        lstm_cell_bw = lstm_cell_type(num_units=self.num_units, activation=self.activation_fn, layer_norm=self.layer_norm, dropout_keep_prob=self.recurrent_dropout, reuse=tf.get_variable_scope().reuse)
        if (not self.separate_directions):
            (outputs_tupple, _) = bidirectional_dynamic_rnn(lstm_cell_fw, lstm_cell_bw, inputs, dtype=tf.float32, sequence_length=sequence_length)
            outputs = tf.concat(outputs_tupple, 2)
        else:
            (outputs, _) = rnn.bidirectional_dynamic_rnn_2inputs(lstm_cell_fw, lstm_cell_bw, inputs[0], inputs[1], dtype=tf.float32, sequence_length=sequence_length)
        return outputs
