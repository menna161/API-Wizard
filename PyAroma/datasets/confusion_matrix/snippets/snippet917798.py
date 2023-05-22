import numpy as np
from medpy import metric


def total_negatives_reference(test=None, reference=None, confusion_matrix=None, **kwargs):
    'TN + FP'
    if (confusion_matrix is None):
        confusion_matrix = ConfusionMatrix(test, reference)
    (tp, fp, tn, fn) = confusion_matrix.get_matrix()
    return (tn + fp)
