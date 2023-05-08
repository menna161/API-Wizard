import numpy as np
from medpy import metric


def true_negative_rate(test=None, reference=None, confusion_matrix=None, nan_for_nonexisting=True, **kwargs):
    'TN / (TN + FP)'
    return specificity(test, reference, confusion_matrix, nan_for_nonexisting)
