import numpy as np
import tensorflow as tf
from keras import layers, backend as K
from keras.losses import Loss
from keras.utils import losses_utils


def call(self, y_true: np.array, y_pred: np.array, sample_weight=None) -> np.array:
    '\n        Calculate rank cross entropy loss.\n\n        :param y_true: Label.\n        :param y_pred: Predicted result.\n        :return: Crossentropy loss computed by user-defined negative number.\n        '
    logits = layers.Lambda((lambda a: a[(::(self._num_neg + 1), :)]))(y_pred)
    labels = layers.Lambda((lambda a: a[(::(self._num_neg + 1), :)]))(y_true)
    (logits, labels) = ([logits], [labels])
    for neg_idx in range(self._num_neg):
        neg_logits = layers.Lambda((lambda a: a[((neg_idx + 1)::(self._num_neg + 1), :)]))(y_pred)
        neg_labels = layers.Lambda((lambda a: a[((neg_idx + 1)::(self._num_neg + 1), :)]))(y_true)
        logits.append(neg_logits)
        labels.append(neg_labels)
    logits = tf.concat(logits, axis=(- 1))
    labels = tf.concat(labels, axis=(- 1))
    smoothed_prob = (tf.nn.softmax(logits) + np.finfo(float).eps)
    loss = (- tf.reduce_sum((labels * tf.math.log(smoothed_prob)), axis=(- 1)))
    return losses_utils.compute_weighted_loss(loss, sample_weight, reduction=self.reduction)
