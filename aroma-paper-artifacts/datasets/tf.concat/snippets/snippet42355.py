import tensorflow as tf
import numpy as np


def call(self, y_true: tf.Tensor, y_pred: tf.Tensor) -> tf.Tensor:
    ' NOTE : y_pred must be cos similarity\n\n    Args:\n        y_true (tf.Tensor): shape [batch,ndim]\n        y_pred (tf.Tensor): shape [batch,ndim]\n\n    Returns:\n        tf.Tensor: loss\n    '
    idxs = tf.concat([self.batch_idxs, tf.cast(y_true, tf.int32)], 1)
    sp = tf.expand_dims(tf.gather_nd(y_pred, idxs), 1)
    mask = tf.logical_not(tf.scatter_nd(idxs, tf.ones(tf.shape(idxs)[0], tf.bool), tf.shape(y_pred)))
    sn = tf.reshape(tf.boolean_mask(y_pred, mask), (self.batch_size, (- 1)))
    alpha_p = tf.nn.relu((self.O_p - tf.stop_gradient(sp)))
    alpha_n = tf.nn.relu((tf.stop_gradient(sn) - self.O_n))
    r_sp_m = (alpha_p * (sp - self.Delta_p))
    r_sn_m = (alpha_n * (sn - self.Delta_n))
    _Z = tf.concat([r_sn_m, r_sp_m], 1)
    _Z = (_Z * self.gamma)
    logZ = tf.math.reduce_logsumexp(_Z, 1, keepdims=True)
    return (((- r_sp_m) * self.gamma) + logZ)
