import numpy as np
import scipy.sparse.linalg as sparselinalg
import torch
from DominantSparseEigenAD.eig import DominantEig
import DominantSparseEigenAD.eig as eig
import time


def setparameters(self, initA=None):
    if (initA is None):
        A = torch.randn(self.d, self.D, self.D, dtype=torch.float64)
        print('Random initialization.')
    else:
        A = initA
        print('Initialization using the last optimized result.')
    self.A = torch.nn.Parameter(A)
