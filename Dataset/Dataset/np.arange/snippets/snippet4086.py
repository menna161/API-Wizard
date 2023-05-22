import numpy as np
import tensorflow as tf


def dcg_score(y_true, y_score, k=10):
    'Computing dcg score metric at k.\n\n    Args:\n        y_true (numpy.ndarray): ground-truth labels.\n        y_score (numpy.ndarray): predicted labels.\n\n    Returns:\n        numpy.ndarray: dcg scores.\n    '
    k = min(np.shape(y_true)[1], k)
    order = np.argsort(y_score, axis=1)[(:, ::(- 1))]
    y_true = np.take(y_true, order[(:, :k)])
    gains = ((2 ** y_true) - 1)
    discounts = np.log2((np.arange(np.shape(y_true)[1]) + 2))
    return np.sum((gains / discounts), axis=1)
