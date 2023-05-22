import string
import tensorflow as tf
from tensorflow.python.ops.rnn import bidirectional_dynamic_rnn, dynamic_rnn
from nabu.neuralnetworks.components import ops, rnn_cell, rnn, rnn_cell_impl
from ops import capsule_initializer
from tensorflow.python.ops import gen_nn_ops
from tensorflow.python.framework import ops


def __call__(self, inputs_for_forward, inputs_for_backward, sequence_length, scope=None):
    '\n\t\tCreate the variables and do the forward computation\n\n\t\tArgs:\n\t\t\tinputs: the input to the layer as a\n\t\t\t\t[batch_size, max_length, dim] tensor\n\t\t\tsequence_length: the length of the input sequences as a\n\t\t\t\t[batch_size] tensor\n\t\t\tscope: The variable scope sets the namespace under which\n\t\t\t\tthe variables created during this call will be stored.\n\n\t\tReturns:\n\t\t\tthe output of the layer\n\t\t'
    if (inputs_for_backward is None):
        inputs_for_backward = inputs_for_forward
    batch_size = inputs_for_forward.get_shape()[0]
    max_length = tf.shape(inputs_for_forward)[1]
    with tf.variable_scope((scope or type(self).__name__)):
        if (self.group_size == 1):
            gru_cell_fw = rnn_cell_impl.ResetGRUCell(num_units=self.num_units, t_reset=self.t_reset, activation=self.activation_fn, reuse=tf.get_variable_scope().reuse)
            gru_cell_bw = rnn_cell_impl.ResetGRUCell(num_units=self.num_units, t_reset=self.t_reset, activation=self.activation_fn, reuse=tf.get_variable_scope().reuse)
            tile_shape = [1, 1, self.t_reset, 1]
        else:
            gru_cell_fw = rnn_cell_impl.GroupResetGRUCell(num_units=self.num_units, t_reset=self.t_reset, group_size=self.group_size, activation=self.activation_fn, reuse=tf.get_variable_scope().reuse)
            gru_cell_bw = rnn_cell_impl.GroupResetGRUCell(num_units=self.num_units, t_reset=self.t_reset, group_size=self.group_size, activation=self.activation_fn, reuse=tf.get_variable_scope().reuse)
            tile_shape = [1, 1, gru_cell_fw._num_replicates, 1]
        (outputs_tupple, _) = rnn.bidirectional_dynamic_rnn_2inputs_time_input(gru_cell_fw, gru_cell_bw, inputs_for_forward, inputs_for_backward, dtype=tf.float32, sequence_length=sequence_length)
        actual_outputs_forward = outputs_tupple[0][0]
        actual_outputs_backward = outputs_tupple[1][0]
        actual_outputs = tf.concat((actual_outputs_forward, actual_outputs_backward), (- 1))
        forward_replicas = outputs_tupple[0][1]
        backward_replicas = outputs_tupple[1][1]
        if (not self.symmetric_context):
            forward_for_backward = tf.expand_dims(actual_outputs_forward, (- 2))
            forward_for_backward = tf.tile(forward_for_backward, tile_shape)
            backward_for_forward = tf.expand_dims(actual_outputs_backward, (- 2))
            backward_for_forward = tf.tile(backward_for_forward, tile_shape)
            outputs_for_forward = tf.concat((forward_replicas, backward_for_forward), (- 1))
            outputs_for_backward = tf.concat((forward_for_backward, backward_replicas), (- 1))
        else:
            T = tf.to_int32(tf.ceil((tf.to_float(sequence_length) / tf.to_float(self.group_size))))
            T_min_1 = tf.expand_dims((T - 1), (- 1))
            numbers_to_maxT = tf.range(0, max_length)
            numbers_to_maxT = tf.expand_dims(tf.expand_dims(numbers_to_maxT, 0), (- 1))
            numbers_to_k = tf.expand_dims(range(0, self.num_replicates), 0)
            backward_indices_for_forward_t_0 = (numbers_to_k + T_min_1)
            backward_indices_for_forward_t_0 = tf.expand_dims(backward_indices_for_forward_t_0, 1)
            backward_indices_for_forward_t = tf.mod((backward_indices_for_forward_t_0 - (2 * numbers_to_maxT)), self.num_replicates)
            forward_indices_for_backward_t_0 = (numbers_to_k - T_min_1)
            forward_indices_for_backward_t_0 = tf.expand_dims(forward_indices_for_backward_t_0, 1)
            forward_indices_for_backward_t = tf.mod((forward_indices_for_backward_t_0 + (2 * numbers_to_maxT)), self.num_replicates)
            ra1 = tf.range(batch_size)
            ra1 = tf.expand_dims(tf.expand_dims(ra1, (- 1)), (- 1))
            ra1 = tf.tile(ra1, [1, max_length, self.num_replicates])
            ra2 = tf.range(max_length)
            ra2 = tf.expand_dims(tf.expand_dims(ra2, 0), (- 1))
            ra2 = tf.tile(ra2, [batch_size, 1, self.num_replicates])
            stacked_backward_indices_for_forward_t = tf.stack([ra1, ra2, backward_indices_for_forward_t], axis=(- 1))
            backward_for_forward = tf.gather_nd(backward_replicas, stacked_backward_indices_for_forward_t)
            stacked_forward_indices_for_backward_t = tf.stack([ra1, ra2, forward_indices_for_backward_t], axis=(- 1))
            forward_for_backward = tf.gather_nd(forward_replicas, stacked_forward_indices_for_backward_t)
            outputs_for_forward = tf.concat((forward_replicas, backward_for_forward), (- 1))
            outputs_for_backward = tf.concat((forward_for_backward, backward_replicas), (- 1))
        outputs = (actual_outputs, outputs_for_forward, outputs_for_backward)
        return outputs
