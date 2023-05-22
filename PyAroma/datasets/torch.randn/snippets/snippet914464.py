import time, pytest
import torch
from DominantSparseEigenAD.CG import CG_torch
import numpy as np
from scipy.stats import ortho_group
import numpy as np
from scipy.stats import ortho_group


def test_fullrank():
    import numpy as np
    from scipy.stats import ortho_group
    n = 100
    diagonal = (1.0 + (10.0 * np.random.rand(n)))
    U = ortho_group.rvs(n)
    '\n        A is randomly generated as a real, symmetric, positive definite matrix\n    of size n*n.\n    '
    A = U.dot(np.diag(diagonal)).dot(U.T)
    A = torch.from_numpy(A).to(torch.float64)
    print('\n----- test_fullrank -----')
    print(('----- Dimension of matrix A: %d -----' % n))
    b = torch.randn(n, dtype=torch.float64)
    initialx = torch.randn(n, dtype=torch.float64)
    start = time.time()
    x = CG_torch(A, b, initialx)
    end = time.time()
    print('CG_torch time: ', (end - start))
    assert torch.allclose(A.matmul(x), b)
