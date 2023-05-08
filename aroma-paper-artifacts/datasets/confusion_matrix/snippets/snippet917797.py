import numpy as np
from medpy import metric


def total_positives_reference(test=None, reference=None, confusion_matrix=None, **kwargs):
    'TP + FN'
    if (confusion_matrix is None):
        confusion_matrix = ConfusionMatrix(test, reference)
    (tp, fp, tn, fn) = confusion_matrix.get_matrix()
    return (tp + fn)
