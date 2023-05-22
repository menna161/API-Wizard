import pytest
import time
import torch
from DominantSparseEigenAD.Lanczos import symeigLanczos
import numpy as np


def test_normal_tridiagonal():
    import numpy as np
    (xmin, xmax, N) = ((- 1.0), 1.0, 1000)
    xmesh = np.linspace(xmin, xmax, num=N, endpoint=False)
    xmesh = torch.from_numpy(xmesh).to(torch.float64)
    h = ((xmax - xmin) / N)
    K = (((- 0.5) / (h ** 2)) * ((torch.diag(((- 2) * torch.ones(N, dtype=xmesh.dtype))) + torch.diag(torch.ones((N - 1), dtype=xmesh.dtype), diagonal=1)) + torch.diag(torch.ones((N - 1), dtype=xmesh.dtype), diagonal=(- 1))))
    potential = (0.5 * (xmesh ** 2))
    V = torch.diag(potential)
    Hmatrix = (K + V)
    k = 1000
    start = time.time()
    (E0, psi0) = symeigLanczos(Hmatrix, k, extreme='min')
    end = time.time()
    print('\n----- test_normal_tridiagonal -----')
    print('Lanczos: ', (end - start))
    start = time.time()
    (Es, psis) = torch.symeig(Hmatrix, eigenvectors=True)
    end = time.time()
    print('Pytorch: ', (end - start))
    assert torch.allclose(E0, Es[0])
    assert (torch.allclose(psi0, psis[(:, 0)]) or torch.allclose(psi0, (- psis[(:, 0)])))
