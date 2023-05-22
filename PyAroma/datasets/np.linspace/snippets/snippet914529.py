import numpy as np
import torch
from DominantSparseEigenAD.Lanczos import symeigLanczos
import matplotlib.pyplot as plt


def H1(N):
    (xmin, xmax) = ((- 1.0), 1.0)
    xmesh = np.linspace(xmin, xmax, num=N, endpoint=False)
    xmesh = torch.from_numpy(xmesh).to(torch.float64)
    h = ((xmax - xmin) / N)
    K = (((- 0.5) / (h ** 2)) * ((torch.diag(((- 2) * torch.ones(N, dtype=xmesh.dtype))) + torch.diag(torch.ones((N - 1), dtype=xmesh.dtype), diagonal=1)) + torch.diag(torch.ones((N - 1), dtype=xmesh.dtype), diagonal=(- 1))))
    potential = (0.5 * (xmesh ** 2))
    V = torch.diag(potential)
    Hmatrix = (K + V)
    return Hmatrix
