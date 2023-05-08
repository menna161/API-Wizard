import numpy as np


def __init__(self, n_classes):
    self.n_classes = n_classes
    self.confusion_matrix = np.zeros((n_classes, n_classes))
