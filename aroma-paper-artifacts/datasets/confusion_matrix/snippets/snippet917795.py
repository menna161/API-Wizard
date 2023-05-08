import numpy as np
from medpy import metric


def total_positives_test(test=None, reference=None, confusion_matrix=None, **kwargs):
    'TP + FP'
    if (confusion_matrix is None):
        confusion_matrix = ConfusionMatrix(test, reference)
    (tp, fp, tn, fn) = confusion_matrix.get_matrix()
    return (tp + fp)
