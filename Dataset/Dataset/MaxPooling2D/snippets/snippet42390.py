import numpy as np
from keras import backend as K
from keras import activations
from keras.layers import Recurrent, Conv2D, UpSampling2D, MaxPooling2D, Dense, Subtract, Concatenate, Flatten
from keras.engine import InputSpec


def build(self, input_shape):
    self.input_spec = [InputSpec(shape=input_shape)]
    self.conv_layers = {c: [] for c in ['i', 'f', 'c', 'o', 'a', 'ahat']}
    self.e_up_layers = []
    self.e_down_layers = []
    self.e_layers = []
    for l in range(self.nb_layers):
        for c in ['i', 'f', 'c', 'o']:
            act = (self.LSTM_activation if (c == 'c') else self.LSTM_inner_activation)
            self.conv_layers[c].append(Conv2D(self.R_stack_sizes[l], self.R_filt_sizes[l], padding='same', activation=act, data_format=self.data_format))
        act = ('relu' if (l == 0) else self.A_activation)
        self.conv_layers['ahat'].append(Conv2D(self.stack_sizes[l], self.Ahat_filt_sizes[l], padding='same', activation=act, data_format=self.data_format))
        if (l < (self.nb_layers - 1)):
            self.conv_layers['a'].append(Conv2D(self.stack_sizes[(l + 1)], self.A_filt_sizes[l], padding='same', activation=self.A_activation, data_format=self.data_format))
    self.upsample = UpSampling2D(data_format=self.data_format)
    self.pool = MaxPooling2D(data_format=self.data_format)
    self.trainable_weights = []
    (nb_row, nb_col) = ((input_shape[(- 2)], input_shape[(- 1)]) if (self.data_format == 'channels_first') else (input_shape[(- 3)], input_shape[(- 2)]))
    for c in sorted(self.conv_layers.keys()):
        for l in range(len(self.conv_layers[c])):
            ds_factor = (2 ** l)
            if (c == 'ahat'):
                nb_channels = self.R_stack_sizes[l]
            elif (c == 'a'):
                nb_channels = (2 * self.R_stack_sizes[l])
            else:
                nb_channels = ((self.stack_sizes[l] * 2) + self.R_stack_sizes[l])
                if (l < (self.nb_layers - 1)):
                    nb_channels += self.R_stack_sizes[(l + 1)]
            in_shape = (input_shape[0], nb_channels, (nb_row // ds_factor), (nb_col // ds_factor))
            if (self.data_format == 'channels_last'):
                in_shape = (in_shape[0], in_shape[2], in_shape[3], in_shape[1])
            if (c == 'ahat'):
                self.e_down_layers.append(Subtract())
                self.e_up_layers.append(Subtract())
                self.e_layers.append(Concatenate())
                with K.name_scope(('layer_e_down_' + str(l))):
                    self.e_down_layers[(- 1)].build([in_shape, in_shape])
                with K.name_scope(('layer_e_up_' + str(l))):
                    self.e_up_layers[(- 1)].build([in_shape, in_shape])
                with K.name_scope(('layer_e_' + str(l))):
                    self.e_layers[(- 1)].build([in_shape, in_shape])
            with K.name_scope(((('layer_' + c) + '_') + str(l))):
                self.conv_layers[c][l].build(in_shape)
            self.trainable_weights += self.conv_layers[c][l].trainable_weights
    self.states = (([None] * self.nb_layers) * 3)
    if (self.extrap_start_time is not None):
        self.t_extrap = K.variable(self.extrap_start_time, (int if (K.backend() != 'tensorflow') else 'int32'))
        self.states += ([None] * 2)
