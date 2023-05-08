import numpy as np


def reset(self):
    self.confusion_matrix = np.zeros((self.n_classes, self.n_classes))
