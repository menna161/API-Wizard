import numpy as np
from sklearn.linear_model import LogisticRegression
from ..utils import metrics


def __init__(self, penalty='l2', C=100, tol=0.01, class_weight=None, max_iter=100):
    ' The Invariants Mining model for anomaly detection\n\n        Attributes\n        ----------\n            classifier: object, the classifier for anomaly detection\n        '
    self.classifier = LogisticRegression(penalty=penalty, C=C, tol=tol, class_weight=class_weight, max_iter=max_iter)
