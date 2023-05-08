import numpy as np
from medpy import metric


def false_discovery_rate(test=None, reference=None, confusion_matrix=None, nan_for_nonexisting=True, **kwargs):
    'FP / (TP + FP)'
    return (1 - precision(test, reference, confusion_matrix, nan_for_nonexisting))
