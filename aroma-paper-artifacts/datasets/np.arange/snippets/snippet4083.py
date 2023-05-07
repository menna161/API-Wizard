import numpy as np
import tensorflow as tf


def mrr_score(y_true, y_score):
    'Computing mrr score metric.\n\n    Args:\n        y_true (numpy.ndarray): ground-truth labels.\n        y_score (numpy.ndarray): predicted labels.\n\n    Returns:\n        numpy.ndarray: mrr scores.\n    '
    order = np.argsort(y_score, axis=1)[(:, ::(- 1))]
    y_true = np.take(y_true, order)
    rr_score = (y_true / (np.arange(np.shape(y_true)[1]) + 1))
    return (np.sum(rr_score, axis=1) / np.sum(y_true, axis=1))
