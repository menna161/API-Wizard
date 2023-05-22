import numpy as np
import torch
from DominantSparseEigenAD.symeig import DominantSymeig


def setparameters(self):
    A = torch.randn(self.d, self.D, self.D, dtype=torch.float64)
    A = (0.5 * (A + A.permute(0, 2, 1)))
    self.A = torch.nn.Parameter(A)
