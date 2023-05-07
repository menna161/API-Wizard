import tensorflow as tf
import model
from nabu.neuralnetworks.components import layer
import numpy as np


def _get_outputs(self, inputs, input_seq_length, is_training):
    '\n\t\tCreate the variables and do the forward computation\n\n\t\tArgs:\n\t\t\tinputs: the inputs to the neural network, this is a list of\n\t\t\t\t[batch_size x time x ...] tensors\n\t\t\tinput_seq_length: The sequence lengths of the input utterances, this\n\t\t\t\tis a [batch_size] vector\n\t\t\tis_training: whether or not the network is in training mode\n\n\t\tReturns:\n\t\t\t- output, which is a [batch_size x time x ...] tensors\n\t\t'
    num_units = int(self.conf['num_units'])
    num_lay = int(self.conf['num_layers'])
    t_resets = self.conf['t_reset']
    t_resets = t_resets.split(' ')
    if (len(t_resets) == 1):
        t_resets = (t_resets * num_lay)
    t_resets = map(int, t_resets)
    if any([(t_resets[(l + 1)] < t_resets[l]) for l in range((num_lay - 1))]):
        raise ValueError('T_reset in next layer must be equal to or bigger than T_reset in current layer')
    if ('group_size' in self.conf):
        group_sizes = self.conf['group_size']
        group_sizes = group_sizes.split(' ')
    else:
        group_sizes = '1'
    if (len(group_sizes) == 1):
        group_sizes = (group_sizes * num_lay)
    group_sizes = map(int, group_sizes)
    if any([(np.mod(t_res, group_size) != 0) for (t_res, group_size) in zip(t_resets, group_sizes)]):
        raise ValueError('t_reset should be a multiple of group_size')
    if ('forward_reset' in self.conf):
        forward_reset = (self.conf['forward_reset'] == 'True')
    else:
        forward_reset = True
    if ('backward_reset' in self.conf):
        backward_reset = (self.conf['backward_reset'] == 'True')
    else:
        backward_reset = True
    if ('separate_directions' in self.conf):
        separate_directions = (self.conf['separate_directions'] == 'True')
    else:
        separate_directions = False
    layer_norm = (self.conf['layer_norm'] == 'True')
    recurrent_dropout = float(self.conf['recurrent_dropout'])
    if ('activation_fn' in self.conf):
        if (self.conf['activation_fn'] == 'tanh'):
            activation_fn = tf.nn.tanh
        elif (self.conf['activation_fn'] == 'relu'):
            activation_fn = tf.nn.relu
        elif (self.conf['activation_fn'] == 'sigmoid'):
            activation_fn = tf.nn.sigmoid
        else:
            raise Exception(('Undefined activation function: %s' % self.conf['activation_fn']))
    else:
        activation_fn = tf.nn.tanh
    if (len(inputs) > 1):
        raise Exception(('The implementation of DBLSTM expects 1 input and not %d' % len(inputs)))
    else:
        inputs = inputs[0]
    with tf.variable_scope(self.scope):
        if (is_training and (float(self.conf['input_noise']) > 0)):
            inputs = (inputs + tf.random_normal(tf.shape(inputs), stddev=float(self.conf['input_noise'])))
        logits = inputs
        for l in range(num_lay):
            blstm = layer.BResetLSTMLayer(num_units=num_units, t_reset=t_resets[l], group_size=group_sizes[l], forward_reset=forward_reset, backward_reset=backward_reset, layer_norm=layer_norm, recurrent_dropout=recurrent_dropout, activation_fn=activation_fn)
            if (l == 0):
                multistate_input = tf.expand_dims(logits, 2)
                num_replicates = int((float(t_resets[l]) / float(group_sizes[l])))
                multistate_input = tf.tile(multistate_input, tf.constant([1, 1, num_replicates, 1]))
                if forward_reset:
                    for_forward = multistate_input
                else:
                    for_forward = logits
                if backward_reset:
                    for_backward = multistate_input
                else:
                    for_backward = logits
            else:
                (for_forward, for_backward) = permute_versions(logits_multistate, logits, input_seq_length, t_resets[l], t_resets[(l - 1)], group_sizes[l], group_sizes[(l - 1)], forward_reset, backward_reset, separate_directions)
            (logits, logits_multistate) = blstm(for_forward, for_backward, input_seq_length, ('layer' + str(l)))
        if (is_training and (float(self.conf['dropout']) < 1)):
            raise Exception('dropout not yet implemented for state reset lstm')
        output = tf.concat(logits, (- 1))
    return output
