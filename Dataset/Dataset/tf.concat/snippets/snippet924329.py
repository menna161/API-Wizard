from .layers import *


def ber_concrete(temp, p_logits, n_samples=None):
    shape = (tf.shape(p_logits) if (n_samples is None) else tf.concat([[n_samples], tf.shape(p_logits)], 0))
    u = tf.random_uniform(shape)
    return sigmoid(((logit(u) + p_logits) / temp))
