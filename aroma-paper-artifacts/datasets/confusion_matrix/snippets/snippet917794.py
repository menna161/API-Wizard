import numpy as np
from medpy import metric


def negative_predictive_value(test=None, reference=None, confusion_matrix=None, nan_for_nonexisting=True, **kwargs):
    'TN / (TN + FN)'
    return (1 - false_omission_rate(test, reference, confusion_matrix, nan_for_nonexisting))
