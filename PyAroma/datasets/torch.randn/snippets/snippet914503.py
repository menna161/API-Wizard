import numpy as np
import torch
import time


def contraction_torch(d, D):
    print('----- Pytorch -----')
    A = torch.randn(d, D, D, dtype=torch.float64)
    start = time.time()
    Gong = torch.einsum('kij,kmn->imjn', A, A).reshape((D ** 2), (D ** 2))
    end = time.time()
    print('constructig Gong: (~ D^4 * d)\t', (end - start))
    r = torch.randn(D, D, dtype=torch.float64)
    r_flat = r.reshape((D ** 2))
    start = time.time()
    '\n        method1: matrix multiplication.\n        ~ D^4\n    '
    result1 = Gong.matmul(r_flat)
    end = time.time()
    print('method1: (~ D^4)\t\t', (end - start))
    start = time.time()
    '\n        method2: (manual) optimized einsum.\n        ~ D^3 * d\n    '
    intermediate = torch.einsum('kij,jn->kin', A, r)
    result2 = torch.einsum('kin,kmn->im', intermediate, A).reshape((D ** 2))
    end = time.time()
    print('method2: (~D^3 * d)\t\t', (end - start))
    start = time.time()
    '\n        method3: native torch einsum (not optimized).\n        ~ D^4 * d + D^4. i.e., roughly equal to the cost of the construction of the \n    matrix Gong and the matrix multiplication process(method 1).\n    '
    result3 = torch.einsum('kij,kmn,jn->im', A, A, r).reshape((D ** 2))
    end = time.time()
    print('method3: (~ D^4 * d + D^4)\t', (end - start))
    assert torch.allclose(result1, result2)
    assert torch.allclose(result1, result3)
