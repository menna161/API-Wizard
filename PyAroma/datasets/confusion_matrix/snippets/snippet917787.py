import numpy as np
from medpy import metric


def accuracy(test=None, reference=None, confusion_matrix=None, **kwargs):
    '(TP + TN) / (TP + FP + FN + TN)'
    if (confusion_matrix is None):
        confusion_matrix = ConfusionMatrix(test, reference)
    (tp, fp, tn, fn) = confusion_matrix.get_matrix()
    return float(((tp + tn) / (((tp + fp) + tn) + fn)))
