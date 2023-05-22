import tensorflow as tf
import model
import numpy as np


def _get_outputs(self, inputs, input_seq_length=None, is_training=None):
    '\n\t\tconcatenate the inputs over the last dimension.\n\n\t\tArgs:\n\t\t\tinputs: the inputs to concatenate, this is a list of\n\t\t\t\t[batch_size x time x ...] tensors and/or [batch_size x ...] tensors\n\t\t\tinput_seq_length: None\n\t\t\tis_training: None\n\n\t\tReturns:\n\t\t\t- outputs, the concatenated inputs\n\t\t'
    if ('select_inputs' in self.conf):
        select_inputs = self.conf['select_inputs'].split(' ')
        select_inputs = [(sel == 'True') for sel in select_inputs]
    else:
        select_inputs = ([True] * len(inputs))
    if ('flatten_last_2_dims' in self.conf):
        flatten_last_2_dims = self.conf['flatten_last_2_dims'].split(' ')
        flatten_last_2_dims = [(flat == 'True') for flat in flatten_last_2_dims]
    else:
        flatten_last_2_dims = ([False] * len(inputs))
    if ('expand_dim_to_first_input' in self.conf):
        expand_dim_to_first_input = self.conf['expand_dim_to_first_input'].split(' ')
        expand_dim_to_first_input = [(exp == 'True') for exp in expand_dim_to_first_input]
    else:
        expand_dim_to_first_input = ([False] + ([True] * (len(inputs) - 1)))
    if ('expand_dimension' in self.conf):
        expand_dimension = int(self.conf['expand_dimension'])
    else:
        expand_dimension = (- 2)
    if (is_training and ('input_noise' in self.conf)):
        inputs_noise = map(float, self.conf['input_noise'].split(' '))
        inputs = [(inp + tf.random_normal(tf.shape(inp), stddev=inp_noise)) for (inp, inp_noise) in zip(inputs, inputs_noise)]
    with tf.variable_scope(self.scope):
        inputs = [inputs[ind] for (ind, sel) in enumerate(select_inputs) if sel]
        flatten_last_2_dims = [flatten_last_2_dims[ind] for (ind, sel) in enumerate(select_inputs) if sel]
        expand_dim_to_first_input = [expand_dim_to_first_input[ind] for (ind, sel) in enumerate(select_inputs) if sel]
        for (ind, inp) in enumerate(inputs):
            if flatten_last_2_dims[ind]:
                inp_shape = tf.shape(inp)
                inp_stat_shape = inp.get_shape().as_list()
                if (None in inp_stat_shape[(- 2):]):
                    raise ValueError('Last two dimensions of tensor should be known before flattening.')
                new_last_shape = (inp_stat_shape[(- 2)] * inp_stat_shape[(- 1)])
                new_shape = tf.concat([inp_shape[:(- 2)], [new_last_shape]], axis=0)
                inputs[ind] = tf.reshape(inp, new_shape)
        if (len(inputs) == 1):
            return inputs[0]
        if expand_dim_to_first_input[0]:
            raise ValueError('The expanded dimension is tiled to match the first input. Therefor it is not possible for the first input')
        else:
            size_of_expanded_dim = tf.shape(inputs[0])[expand_dimension]
            out_dim = len(inputs[0].get_shape())
            multiplicates = np.ones(out_dim, np.int).tolist()
            multiplicates[expand_dimension] = size_of_expanded_dim
            multiplicates = tf.stack(multiplicates)
        for (ind, inp) in enumerate(inputs):
            if expand_dim_to_first_input[ind]:
                inp = tf.expand_dims(inp, expand_dimension)
                inputs[ind] = tf.tile(inp, multiplicates)
        output = tf.concat(inputs, (- 1))
    return output
