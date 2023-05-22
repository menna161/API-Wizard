import time, pytest
import torch
from DominantSparseEigenAD.CG import CG_torch
import numpy as np
from scipy.stats import ortho_group
import numpy as np
from scipy.stats import ortho_group


@pytest.mark.skipif((not torch.cuda.is_available()), reason='No GPU support in online test envionment')
def test_fullrank_gpu():
    import numpy as np
    from scipy.stats import ortho_group
    n = 100
    diagonal = (1.0 + (10.0 * np.random.rand(n)))
    U = ortho_group.rvs(n)
    '\n        A is randomly generated as a real, symmetric, positive definite matrix\n    of size n*n.\n    '
    A = U.dot(np.diag(diagonal)).dot(U.T)
    cuda = torch.device('cuda')
    dtype = torch.float64
    A = torch.from_numpy(A).to(cuda, dtype=dtype)
    b = torch.randn(n, device=cuda, dtype=dtype)
    initialx = torch.randn(n, device=cuda, dtype=dtype)
    x = CG_torch(A, b, initialx)
    groundtruth = torch.inverse(A).matmul(b)
    assert torch.allclose(x, groundtruth)
