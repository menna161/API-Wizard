import numpy as np
from medpy import metric


def fscore(test=None, reference=None, confusion_matrix=None, nan_for_nonexisting=True, beta=1.0, **kwargs):
    '(1 + b^2) * TP / ((1 + b^2) * TP + b^2 * FN + FP)'
    precision_ = precision(test, reference, confusion_matrix, nan_for_nonexisting)
    recall_ = recall(test, reference, confusion_matrix, nan_for_nonexisting)
    return ((((1 + (beta * beta)) * precision_) * recall_) / (((beta * beta) * precision_) + recall_))
