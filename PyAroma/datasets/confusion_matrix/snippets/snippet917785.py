import numpy as np
from medpy import metric


def recall(test=None, reference=None, confusion_matrix=None, nan_for_nonexisting=True, **kwargs):
    'TP / (TP + FN)'
    return sensitivity(test, reference, confusion_matrix, nan_for_nonexisting, **kwargs)
