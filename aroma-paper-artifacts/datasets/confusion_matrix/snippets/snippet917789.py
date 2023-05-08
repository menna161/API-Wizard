import numpy as np
from medpy import metric


def false_positive_rate(test=None, reference=None, confusion_matrix=None, nan_for_nonexisting=True, **kwargs):
    'FP / (FP + TN)'
    return (1 - specificity(test, reference, confusion_matrix, nan_for_nonexisting))
