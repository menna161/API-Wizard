import numpy as np
from medpy import metric


def false_omission_rate(test=None, reference=None, confusion_matrix=None, nan_for_nonexisting=True, **kwargs):
    'FN / (TN + FN)'
    if (confusion_matrix is None):
        confusion_matrix = ConfusionMatrix(test, reference)
    (tp, fp, tn, fn) = confusion_matrix.get_matrix()
    (test_empty, test_full, reference_empty, reference_full) = confusion_matrix.get_existence()
    if test_full:
        if nan_for_nonexisting:
            return float('NaN')
        else:
            return 0.0
    return float((fn / (fn + tn)))
