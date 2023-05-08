import torch
import numpy as np
from scipy.sparse import coo_matrix


def _compute_confusion_matrix(predictions, labels, num_classes):
    if ((np.min(labels) < 0) or (np.max(labels) >= num_classes)):
        raise Exception('Labels out of bound.')
    if ((np.min(predictions) < 0) or (np.max(predictions) >= num_classes)):
        raise Exception('Predictions out of bound.')
    values = np.ones(predictions.shape)
    confusion_matrix = coo_matrix((values, (labels, predictions)), shape=(num_classes, num_classes)).toarray()
    return confusion_matrix
