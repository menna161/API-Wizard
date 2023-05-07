import numpy as np
import tensorflow as tf
from libs.sn import spectral_normed_weight


def deconv2d(input_, output_shape, k_h=4, k_w=4, d_h=2, d_w=2, stddev=None, name='deconv2d', spectral_normed=False, update_collection=None, with_w=False, padding='SAME', mhe=False, net_type='g'):
    fan_in = ((k_h * k_w) * input_.get_shape().as_list()[(- 1)])
    fan_out = ((k_h * k_w) * output_shape[(- 1)])
    if (stddev is None):
        stddev = np.sqrt((2.0 / fan_in))
    with tf.variable_scope(name) as scope:
        if scope_has_variables(scope):
            scope.reuse_variables()
        w = tf.get_variable('w', [k_h, k_w, output_shape[(- 1)], input_.get_shape()[(- 1)]], initializer=tf.truncated_normal_initializer(stddev=stddev))
        if spectral_normed:
            deconv = tf.nn.conv2d_transpose(input_, spectral_normed_weight(w, update_collection=update_collection), output_shape=output_shape, strides=[1, d_h, d_w, 1], padding=padding)
        else:
            deconv = tf.nn.conv2d_transpose(input_, w, output_shape=output_shape, strides=[1, d_h, d_w, 1], padding=padding)
            if mhe:
                eps = 0.0001
                filt = w
                filt_num = input_.get_shape().as_list()[(- 1)]
                filt = tf.reshape(filt, [(- 1), filt_num])
                filt = tf.concat([filt, (- filt)], axis=0)
                filt_norm = tf.sqrt((tf.reduce_sum((filt * filt), [0], keep_dims=True) + eps))
                filt /= filt_norm
                inner_pro = tf.matmul(tf.transpose(filt), filt)
                cross_terms = (2.0 - (2.0 * inner_pro))
                cross_terms = (tf.matrix_band_part(cross_terms, 0, (- 1)) * (1.0 - np.eye(filt_num)))
                loss = ((- 1e-06) * tf.reduce_mean(tf.log((cross_terms + eps))))
                if (net_type == 'g'):
                    tf.add_to_collection('g_mhe_loss', loss)
                else:
                    raise
        biases = tf.get_variable('b', [output_shape[(- 1)]], initializer=tf.constant_initializer(0))
        deconv = tf.reshape(tf.nn.bias_add(deconv, biases), deconv.get_shape())
        if with_w:
            return (deconv, w, biases)
        else:
            return deconv
