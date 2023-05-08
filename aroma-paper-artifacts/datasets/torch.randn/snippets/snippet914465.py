import time, pytest
import torch
from DominantSparseEigenAD.CG import CG_torch
import numpy as np
from scipy.stats import ortho_group
import numpy as np
from scipy.stats import ortho_group


def test_lowrank():
    n = 300
    A = torch.randn(n, n, dtype=torch.float64)
    A = (A + A.T)
    (eigvalues, eigvectors) = torch.symeig(A, eigenvectors=True)
    alpha = eigvalues[0]
    x = eigvectors[(:, 0)]
    Aprime = (A - (alpha * torch.eye(n, dtype=torch.float64)))
    b = torch.randn(n, dtype=torch.float64)
    b = (b - (torch.matmul(x, b) * x))
    initialx = torch.randn(n, dtype=torch.float64)
    initialx = (initialx - (torch.matmul(x, initialx) * x))
    result = CG_torch(Aprime, b, initialx)
    assert torch.allclose((torch.matmul(Aprime, result) - b), torch.zeros(n, dtype=torch.float64), atol=1e-06)
    assert torch.allclose(torch.matmul(result, x)[None], torch.zeros(1, dtype=torch.float64), atol=1e-06)
