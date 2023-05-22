import tensorflow as tf
import model
from nabu.neuralnetworks.components import layer
import numpy as np
import copy
import math


def _get_outputs(self, inputs, input_seq_length, is_training):
    '\n\t\tCreate the variables and do the forward computation\n\n\t\tArgs:\n\t\t\tinputs: the inputs to the neural network, this is a list of\n\t\t\t\t[batch_size x time x ...] tensors\n\t\t\tinput_seq_length: The sequence lengths of the input utterances, this\n\t\t\t\tis a [batch_size] vector\n\t\t\tis_training: whether or not the network is in training mode\n\n\t\tReturns:\n\t\t\t- output, which is a [batch_size x time x ...] tensors\n\t\t'
    if ('filters' in self.conf):
        kernel_size_lay1 = map(int, self.conf['filters'].split(' '))
    elif (('filter_size_t' in self.conf) and ('filter_size_f' in self.conf)):
        kernel_size_t_lay1 = int(self.conf['filter_size_t'])
        kernel_size_f_lay1 = int(self.conf['filter_size_f'])
        kernel_size_lay1 = [kernel_size_t_lay1, kernel_size_f_lay1]
    else:
        raise ValueError('Kernel convolution size not specified.')
    if (('filter_size_t' in self.conf) and ('filter_size_f' in self.conf)):
        kernel_size_t_fac_after_pool = float(self.conf['filter_size_t_fac_after_pool'])
        kernel_size_f_fac_after_pool = float(self.conf['filter_size_f_fac_after_pool'])
        kernel_fac_after_pool = [kernel_size_t_fac_after_pool, kernel_size_f_fac_after_pool]
    else:
        kernel_fac_after_pool = [1, 1]
    f_pool_rate = int(self.conf['f_pool_rate'])
    t_pool_rate = int(self.conf['t_pool_rate'])
    num_encoder_layers = int(self.conf['num_encoder_layers'])
    if (t_pool_rate <= num_encoder_layers):
        raise BaseException('Expecting that not time pooling takes place. Need to adapt input sequence length tensor for lstm part if time pooling is wanted')
    num_decoder_layers = num_encoder_layers
    num_filters_1st_layer = int(self.conf['num_filters_1st_layer'])
    fac_per_layer = float(self.conf['fac_per_layer'])
    num_filters_enc = [int(math.ceil((num_filters_1st_layer * (fac_per_layer ** l)))) for l in range(num_encoder_layers)]
    num_filters_dec = num_filters_enc[::(- 1)]
    num_filters_dec = (num_filters_dec[1:] + [int(self.conf['num_output_filters'])])
    kernel_size_enc = []
    ideal_kernel_size_enc = [kernel_size_lay1]
    bypass = self.conf['bypass']
    layer_norm = (self.conf['layer_norm'] == 'True')
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
        activation_fn = tf.nn.relu
    lstm_num_layers = int(self.conf['lstm_num_layers'])
    lstm_num_units_first_layer = int(self.conf['lstm_num_units'])
    if ('lstm_fac_per_layer' in self.conf):
        lstm_fac_per_layer = float(self.conf['lstm_fac_per_layer'])
    else:
        lstm_fac_per_layer = 1.0
    lstm_num_units = [int(math.ceil((lstm_num_units_first_layer * (lstm_fac_per_layer ** l)))) for l in range(lstm_num_layers)]
    recurrent_dropout = float(self.conf['recurrent_dropout'])
    if ('lstm_activation_fn' in self.conf):
        if (self.conf['lstm_activation_fn'] == 'tanh'):
            lstm_activation_fn = tf.nn.tanh
        elif (self.conf['lstm_activation_fn'] == 'relu'):
            lstm_activation_fn = tf.nn.relu
        elif (self.conf['lstm_activation_fn'] == 'sigmoid'):
            lstm_activation_fn = tf.nn.sigmoid
        else:
            raise Exception(('Undefined LSTM activation function: %s' % self.conf['lstm_activation_fn']))
    else:
        lstm_activation_fn = tf.nn.tanh
    separate_directions = False
    if (('separate_directions' in self.conf) and (self.conf['separate_directions'] == 'True')):
        separate_directions = True
    encoder_layers = []
    for l in range(num_encoder_layers):
        kernel_size_l = copy.deepcopy(ideal_kernel_size_enc[l])
        kernel_size_l_plus_1 = kernel_size_l
        kernel_size_l = [int(math.ceil(k)) for k in kernel_size_l]
        kernel_size_enc.append(kernel_size_l)
        num_filters_l = num_filters_enc[l]
        max_pool_filter = [1, 1]
        if (np.mod((l + 1), t_pool_rate) == 0):
            max_pool_filter[0] = 2
            kernel_size_l_plus_1[0] = (kernel_size_l_plus_1[0] * kernel_fac_after_pool[0])
        if (np.mod((l + 1), f_pool_rate) == 0):
            max_pool_filter[1] = 2
            kernel_size_l_plus_1[1] = (kernel_size_l_plus_1[1] * kernel_fac_after_pool[1])
        ideal_kernel_size_enc.append(kernel_size_l_plus_1)
        encoder_layers.append(layer.Conv2D(num_filters=num_filters_l, kernel_size=kernel_size_l, strides=(1, 1), padding='same', activation_fn=activation_fn, layer_norm=layer_norm, max_pool_filter=max_pool_filter))
    blstm_layers = []
    for l in range(lstm_num_layers):
        blstm_layers.append(layer.BLSTMLayer(num_units=lstm_num_units[l], layer_norm=layer_norm, recurrent_dropout=recurrent_dropout, activation_fn=lstm_activation_fn, separate_directions=separate_directions, fast_version=False))
    decoder_layers = []
    for l in range(num_decoder_layers):
        corresponding_encoder_l = ((num_encoder_layers - 1) - l)
        num_filters_l = num_filters_dec[l]
        kernel_size_l = kernel_size_enc[corresponding_encoder_l]
        if (bypass == 'unpool'):
            strides = [1, 1]
        else:
            strides = encoder_layers[corresponding_encoder_l].max_pool_filter
        decoder_layers.append(layer.Conv2D(num_filters=num_filters_l, kernel_size=kernel_size_l, strides=strides, padding='same', activation_fn=activation_fn, layer_norm=layer_norm, max_pool_filter=(1, 1), transpose=True))
    if (len(inputs) > 1):
        raise ('The implementation of DCNN expects 1 input and not %d' % len(inputs))
    else:
        inputs = inputs[0]
    if (((num_encoder_layers + lstm_num_layers) + num_decoder_layers) == 0):
        output = inputs
        return output
    inputs = tf.expand_dims(inputs, (- 1))
    with tf.variable_scope(self.scope):
        if (is_training and (float(self.conf['input_noise']) > 0)):
            inputs = (inputs + tf.random_normal(tf.shape(inputs), stddev=float(self.conf['input_noise'])))
        logits = inputs
        with tf.variable_scope('encoder'):
            encoder_outputs = []
            encoder_outputs_before_pool = []
            for l in range(num_encoder_layers):
                with tf.variable_scope(('layer_%s' % l)):
                    (logits, outputs_before_pool) = encoder_layers[l](logits)
                    encoder_outputs.append(logits)
                    encoder_outputs_before_pool.append(outputs_before_pool)
                    if (is_training and (float(self.conf['dropout']) < 1)):
                        raise Exception('have to check whether dropout is implemented correctly')
        with tf.variable_scope('lstm_centre'):
            [batch_size, _, new_freq_dim, num_chan] = logits.get_shape()
            logits = tf.transpose(logits, [0, 2, 1, 3])
            logits = tf.reshape(logits, [(batch_size * new_freq_dim), (- 1), num_chan])
            tmp_input_seq_length = tf.expand_dims(input_seq_length, 1)
            tmp_input_seq_length = tf.tile(tmp_input_seq_length, [1, new_freq_dim])
            tmp_input_seq_length = tf.reshape(tmp_input_seq_length, [(batch_size * new_freq_dim)])
            for l in range(lstm_num_layers):
                with tf.variable_scope(('layer_%s' % l)):
                    logits = blstm_layers[l](logits, tmp_input_seq_length)
                    if (is_training and (float(self.conf['dropout']) < 1)):
                        raise Exception('have to check whether dropout is implemented correctly')
            logits = tf.reshape(logits, [batch_size, new_freq_dim, (- 1), (2 * lstm_num_units[(- 1)])])
            logits = tf.transpose(logits, [0, 2, 1, 3])
        with tf.variable_scope('decoder'):
            for l in range(num_decoder_layers):
                with tf.variable_scope(('layer_%s' % l)):
                    corresponding_encoder_l = ((num_encoder_layers - 1) - l)
                    corresponding_encoder_output = encoder_outputs[corresponding_encoder_l]
                    corresponding_encoder_output_before_pool = encoder_outputs_before_pool[corresponding_encoder_l]
                    corresponding_encoder_max_pool_filter = encoder_layers[corresponding_encoder_l].max_pool_filter
                    if ((bypass == 'True') and ((lstm_num_layers > 0) or (l > 0))):
                        decoder_input = tf.concat([logits, corresponding_encoder_output], (- 1))
                    else:
                        decoder_input = logits
                    if ((bypass == 'unpool') and (corresponding_encoder_max_pool_filter != [1, 1])):
                        decoder_input = layer.unpool(pool_input=corresponding_encoder_output_before_pool, pool_output=corresponding_encoder_output, unpool_input=decoder_input, pool_kernel_size=corresponding_encoder_max_pool_filter, pool_stride=corresponding_encoder_max_pool_filter, padding='VALID')
                    (logits, _) = decoder_layers[l](decoder_input)
                    if (is_training and (float(self.conf['dropout']) < 1)):
                        raise Exception('have to check whether dropout is implemented correctly')
                    if (corresponding_encoder_l == 0):
                        wanted_size = tf.shape(inputs)
                    else:
                        wanted_size = tf.shape(encoder_outputs[(corresponding_encoder_l - 1)])
                    wanted_t_size = wanted_size[1]
                    wanted_f_size = wanted_size[2]
                    output_size = tf.shape(logits)
                    output_t_size = output_size[1]
                    output_f_size = output_size[2]
                    missing_t_size = (wanted_t_size - output_t_size)
                    missing_f_size = (wanted_f_size - output_f_size)
                    last_t_slice = tf.expand_dims(logits[(:, (- 1), :, :)], 1)
                    duplicate_logits = tf.tile(last_t_slice, [1, missing_t_size, 1, 1])
                    logits = tf.concat([logits, duplicate_logits], 1)
                    last_f_slice = tf.expand_dims(logits[(:, :, (- 1), :)], 2)
                    duplicate_logits = tf.tile(last_f_slice, [1, 1, missing_f_size, 1])
                    logits = tf.concat([logits, duplicate_logits], 2)
        dyn_shape = logits.get_shape().as_list()
        dyn_shape[(- 2)] = inputs.get_shape()[(- 2)]
        logits.set_shape(dyn_shape)
        output = logits
    return output
