import torch
import numpy as np
from scipy.sparse import coo_matrix


def reset(self):
    'Resets the internal evaluation result to initial state.'
    self.confusion_matrix = 0
