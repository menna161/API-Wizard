import tensorflow as tf
import numpy as np
from dps import cfg
from dps.utils import Param, prime_factors
from dps.utils.tf import ConvNet, ScopedFunction, MLP, apply_mask_and_group_at_front, tf_shape, apply_object_wise


def _call(self, signal, is_training, memory=None):
    if (not self.is_built):
        self.query_funcs = [self.build_mlp(scope='query_head_{}'.format(j)) for j in range(self.n_heads)]
        self.key_funcs = [self.build_mlp(scope='key_head_{}'.format(j)) for j in range(self.n_heads)]
        self.value_funcs = [self.build_mlp(scope='value_head_{}'.format(j)) for j in range(self.n_heads)]
        self.after_func = self.build_mlp(scope='after')
        if self.do_object_wise:
            self.object_wise_func = self.build_object_wise(scope='object_wise')
        if (self.memory is not None):
            self.K = [apply_object_wise(self.key_funcs[j], memory, output_size=self.key_dim, is_training=is_training) for j in range(self.n_heads)]
            self.V = [apply_object_wise(self.value_funcs[j], memory, output_size=self.value_dim, is_training=is_training) for j in range(self.n_heads)]
        self.is_built = True
    n_signal_dim = len(signal.shape)
    assert (n_signal_dim in [2, 3])
    if isinstance(memory, tuple):
        (K, V) = memory
    elif (memory is not None):
        K = [apply_object_wise(self.key_funcs[j], memory, output_size=self.key_dim, is_training=is_training) for j in range(self.n_heads)]
        V = [apply_object_wise(self.value_funcs[j], memory, output_size=self.value_dim, is_training=is_training) for j in range(self.n_heads)]
    elif (self.K is not None):
        K = self.K
        V = self.V
    else:
        K = [apply_object_wise(self.key_funcs[j], signal, output_size=self.key_dim, is_training=is_training) for j in range(self.n_heads)]
        V = [apply_object_wise(self.value_funcs[j], signal, output_size=self.value_dim, is_training=is_training) for j in range(self.n_heads)]
    head_outputs = []
    for j in range(self.n_heads):
        Q = apply_object_wise(self.query_funcs[j], signal, output_size=self.key_dim, is_training=is_training)
        if (n_signal_dim == 2):
            Q = Q[(:, None, :)]
        attention_logits = (tf.matmul(Q, K[j], transpose_b=True) / tf.sqrt(tf.to_float(self.key_dim)))
        attention = tf.nn.softmax(attention_logits)
        attended = tf.matmul(attention, V[j])
        if (n_signal_dim == 2):
            attended = attended[(:, 0, :)]
        head_outputs.append(attended)
    head_outputs = tf.concat(head_outputs, axis=(- 1))
    output = apply_object_wise(self.after_func, head_outputs, output_size=self.n_hidden, is_training=is_training)
    output = tf.layers.dropout(output, self.p_dropout, training=is_training)
    signal = tf.contrib.layers.layer_norm((signal + output))
    if self.do_object_wise:
        output = apply_object_wise(self.object_wise_func, signal, output_size=self.n_hidden, is_training=is_training)
        output = tf.layers.dropout(output, self.p_dropout, training=is_training)
        signal = tf.contrib.layers.layer_norm((signal + output))
    return signal
