import time, pytest
import torch
from DominantSparseEigenAD.CG import CG_torch
import numpy as np
from scipy.stats import ortho_group
import numpy as np
from scipy.stats import ortho_group


@pytest.mark.skipif((not torch.cuda.is_available()), reason='No GPU support in online test envionment')
def test_lowrank_gpu():
    n = 300
    cuda = torch.device('cuda')
    dtype = torch.float64
    A = torch.randn(n, n, device=cuda, dtype=dtype)
    A = (A + A.T)
    (eigvalues, eigvectors) = torch.symeig(A, eigenvectors=True)
    alpha = eigvalues[0]
    x = eigvectors[(:, 0)]
    Aprime = (A - (alpha * torch.eye(n, device=cuda, dtype=dtype)))
    b = torch.randn(n, device=cuda, dtype=dtype)
    b = (b - (torch.matmul(x, b) * x))
    initialx = torch.randn(n, device=cuda, dtype=dtype)
    initialx = (initialx - (torch.matmul(x, initialx) * x))
    result = CG_torch(Aprime, b, initialx)
    assert torch.allclose((torch.matmul(Aprime, result) - b), torch.zeros(n, device=cuda, dtype=dtype), atol=1e-06)
    assert torch.allclose(torch.matmul(result, x)[None], torch.zeros(1, device=cuda, dtype=dtype), atol=1e-06)
