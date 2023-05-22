import numpy as np
from medpy import metric


def specificity(test=None, reference=None, confusion_matrix=None, nan_for_nonexisting=True, **kwargs):
    'TN / (TN + FP)'
    if (confusion_matrix is None):
        confusion_matrix = ConfusionMatrix(test, reference)
    (tp, fp, tn, fn) = confusion_matrix.get_matrix()
    (test_empty, test_full, reference_empty, reference_full) = confusion_matrix.get_existence()
    if reference_full:
        if nan_for_nonexisting:
            return float('NaN')
        else:
            return 0.0
    return float((tn / (tn + fp)))
