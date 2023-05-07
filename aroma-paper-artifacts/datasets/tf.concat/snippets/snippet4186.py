import tensorflow as tf
from tensorflow.keras.initializers import glorot_uniform
from tensorflow.keras.layers import Activation
from tensorflow.keras.regularizers import l2


def call(self, inputs, **kwargs):
    dim = inputs.shape[(- 1)]
    hidden_nn_layers = [inputs]
    final_result = []
    split_tensor0 = tf.split(hidden_nn_layers[0], (dim * [1]), 2)
    for (idx, layer_size) in enumerate(self.layer_size):
        split_tensor = tf.split(hidden_nn_layers[(- 1)], (dim * [1]), 2)
        dot_result_m = tf.matmul(split_tensor0, split_tensor, transpose_b=True)
        dot_result_o = tf.reshape(dot_result_m, shape=[dim, (- 1), (self.field_nums[0] * self.field_nums[idx])])
        dot_result = tf.transpose(dot_result_o, perm=[1, 0, 2])
        curr_out = tf.nn.conv1d(dot_result, filters=self.filters[idx], stride=1, padding='VALID')
        curr_out = tf.nn.bias_add(curr_out, self.bias[idx])
        curr_out = self.activation_layers[idx](curr_out)
        curr_out = tf.transpose(curr_out, perm=[0, 2, 1])
        if self.split_half:
            if (idx != (len(self.layer_size) - 1)):
                (next_hidden, direct_connect) = tf.split(curr_out, (2 * [(layer_size // 2)]), 1)
            else:
                direct_connect = curr_out
                next_hidden = 0
        else:
            direct_connect = curr_out
            next_hidden = curr_out
        final_result.append(direct_connect)
        hidden_nn_layers.append(next_hidden)
    logit = tf.concat(final_result, axis=1)
    logit = tf.reduce_sum(logit, (- 1), keepdims=False)
    return logit
