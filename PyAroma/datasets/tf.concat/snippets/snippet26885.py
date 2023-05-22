import numpy as np
import tensorflow as tf
from keras import layers, backend as K
from keras.losses import Loss
from keras.utils import losses_utils


def call(self, y_true: np.array, y_pred: np.array, sample_weight=None) -> np.array:
    '\n        Calculate rank hinge loss.\n\n        :param y_true: Label.\n        :param y_pred: Predicted result.\n        :return: Hinge loss computed by user-defined margin.\n        '
    y_pos = layers.Lambda((lambda a: a[(::(self._num_neg + 1), :)]), output_shape=(1,))(y_pred)
    y_neg = []
    for neg_idx in range(self._num_neg):
        y_neg.append(layers.Lambda((lambda a: a[((neg_idx + 1)::(self._num_neg + 1), :)]), output_shape=(1,))(y_pred))
    y_neg = tf.concat(y_neg, axis=(- 1))
    y_neg = tf.reduce_mean(y_neg, axis=(- 1), keepdims=True)
    loss = tf.maximum(0.0, ((self._margin + y_neg) - y_pos))
    return losses_utils.compute_weighted_loss(loss, sample_weight, reduction=self.reduction)
