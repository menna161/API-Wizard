import tensorflow as tf
import numpy as np


def call(self, y_true: tf.Tensor, y_pred: tf.Tensor) -> tf.Tensor:
    idxs = tf.concat([self.batch_idxs, tf.cast(y_true, tf.int32)], 1)
    y_true_pred = tf.gather_nd(y_pred, idxs)
    y_true_pred = tf.expand_dims(y_true_pred, 1)
    y_true_pred_margin = (y_true_pred - self.margin)
    _Z = tf.concat([y_pred, y_true_pred_margin], 1)
    _Z = (_Z * self.scale)
    logZ = tf.math.reduce_logsumexp(_Z, 1, keepdims=True)
    logZ = (logZ + tf.math.log((1 - tf.math.exp(((self.scale * y_true_pred) - logZ)))))
    return (((- y_true_pred_margin) * self.scale) + logZ)
