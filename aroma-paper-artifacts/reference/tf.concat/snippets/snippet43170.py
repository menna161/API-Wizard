import tensorflow as tf
import numpy as np
import math


def _add_thomson_constraint(self, filt, n_filt, model, power):
    filt = tf.reshape(filt, [(- 1), n_filt])
    if (model == 'half_mhe'):
        filt_neg = (filt * (- 1))
        filt = tf.concat((filt, filt_neg), axis=1)
        n_filt *= 2
    filt_norm = tf.sqrt((tf.reduce_sum((filt * filt), [0], keep_dims=True) + 0.0001))
    norm_mat = tf.matmul(tf.transpose(filt_norm), filt_norm)
    inner_pro = tf.matmul(tf.transpose(filt), filt)
    inner_pro /= norm_mat
    if (power == '0'):
        cross_terms = (2.0 - (2.0 * inner_pro))
        final = (- tf.log((cross_terms + tf.diag(([1.0] * n_filt)))))
        final -= tf.matrix_band_part(final, (- 1), 0)
        cnt = ((n_filt * (n_filt - 1)) / 2.0)
        loss = ((1 * tf.reduce_sum(final)) / cnt)
    elif (power == '1'):
        cross_terms = ((2.0 - (2.0 * inner_pro)) + tf.diag(([1.0] * n_filt)))
        final = tf.pow(cross_terms, (tf.ones_like(cross_terms) * (- 0.5)))
        final -= tf.matrix_band_part(final, (- 1), 0)
        cnt = ((n_filt * (n_filt - 1)) / 2.0)
        loss = ((1 * tf.reduce_sum(final)) / cnt)
    elif (power == '2'):
        cross_terms = ((2.0 - (2.0 * inner_pro)) + tf.diag(([1.0] * n_filt)))
        final = tf.pow(cross_terms, (tf.ones_like(cross_terms) * (- 1)))
        final -= tf.matrix_band_part(final, (- 1), 0)
        cnt = ((n_filt * (n_filt - 1)) / 2.0)
        loss = ((1 * tf.reduce_sum(final)) / cnt)
    elif (power == 'a0'):
        acos = (tf.acos(inner_pro) / math.pi)
        acos += 0.0001
        final = (- tf.log(acos))
        final -= tf.matrix_band_part(final, (- 1), 0)
        cnt = ((n_filt * (n_filt - 1)) / 2.0)
        loss = ((1 * tf.reduce_sum(final)) / cnt)
    elif (power == 'a1'):
        acos = (tf.acos(inner_pro) / math.pi)
        acos += 0.0001
        final = tf.pow(acos, (tf.ones_like(acos) * (- 1)))
        final -= tf.matrix_band_part(final, (- 1), 0)
        cnt = ((n_filt * (n_filt - 1)) / 2.0)
        loss = ((0.1 * tf.reduce_sum(final)) / cnt)
    elif (power == 'a2'):
        acos = (tf.acos(inner_pro) / math.pi)
        acos += 0.0001
        final = tf.pow(acos, (tf.ones_like(acos) * (- 2)))
        final -= tf.matrix_band_part(final, (- 1), 0)
        cnt = ((n_filt * (n_filt - 1)) / 2.0)
        loss = ((0.1 * tf.reduce_sum(final)) / cnt)
    tf.add_to_collection('thomson_loss', loss)
