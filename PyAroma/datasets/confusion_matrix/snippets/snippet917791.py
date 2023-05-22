import numpy as np
from medpy import metric


def false_negative_rate(test=None, reference=None, confusion_matrix=None, nan_for_nonexisting=True, **kwargs):
    'FN / (TP + FN)'
    return (1 - sensitivity(test, reference, confusion_matrix, nan_for_nonexisting))
