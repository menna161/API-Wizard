import numpy as np
import tensorflow as tf
from libs.sn import spectral_normed_weight


def linear(input_, output_size, name='linear', spectral_normed=False, update_collection=None, stddev=None, bias_start=0.0, with_biases=False, with_w=False, mhe=False, net_type='d'):
    shape = input_.get_shape().as_list()
    if (stddev is None):
        stddev = np.sqrt((1.0 / shape[1]))
    with tf.variable_scope(name) as scope:
        if scope_has_variables(scope):
            scope.reuse_variables()
        weight = tf.get_variable('w', [shape[1], output_size], tf.float32, tf.truncated_normal_initializer(stddev=stddev))
        if with_biases:
            bias = tf.get_variable('b', [output_size], initializer=tf.constant_initializer(bias_start))
        if spectral_normed:
            mul = tf.matmul(input_, spectral_normed_weight(weight, update_collection=update_collection))
        else:
            mul = tf.matmul(input_, weight)
        if mhe:
            eps = 0.0001
            filt = weight
            filt_num = filt.get_shape().as_list()[(- 1)]
            filt = tf.concat([filt, (- filt)], axis=0)
            filt_norm = tf.sqrt((tf.reduce_sum((filt * filt), [0], keep_dims=True) + eps))
            filt /= filt_norm
            inner_pro = tf.matmul(tf.transpose(filt), filt)
            cross_terms = (2.0 - (2.0 * inner_pro))
            cross_terms = (tf.matrix_band_part(cross_terms, 0, (- 1)) * (1.0 - np.eye(filt_num)))
            loss = ((- 1e-07) * tf.reduce_mean(tf.log((cross_terms + eps))))
            if (net_type == 'g'):
                tf.add_to_collection('g_mhe_loss', loss)
            elif (net_type == 'd'):
                tf.add_to_collection('d_mhe_loss', loss)
            else:
                raise
        if with_w:
            if with_biases:
                return ((mul + bias), weight, bias)
            else:
                return (mul, weight, None)
        elif with_biases:
            return (mul + bias)
        else:
            return mul
