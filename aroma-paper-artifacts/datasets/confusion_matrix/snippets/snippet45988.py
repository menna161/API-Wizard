import torch
import numpy as np
from scipy.sparse import coo_matrix


def get(self):
    'Gets the current evaluation result.'
    sum_rows = np.sum(self.confusion_matrix, 0)
    sum_colums = np.sum(self.confusion_matrix, 1)
    diagonal_entries = np.diag(self.confusion_matrix)
    denominator = ((sum_rows + sum_colums) - diagonal_entries)
    valid_classes = (denominator != 0)
    num_valid_classes = np.sum(valid_classes)
    denominator += (1 - valid_classes)
    iou = (diagonal_entries / denominator)
    if (num_valid_classes == 0):
        return float('nan')
    return (np.sum(iou) / num_valid_classes)
