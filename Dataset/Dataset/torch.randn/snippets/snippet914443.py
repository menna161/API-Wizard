import torch


def Lanczos(A, k, device=torch.device('cpu'), *, sparse=False, dim=None):
    '\n        Lanczos iteration algorithm on a real symmetric matrix using Pytorch.\n\n    Input: `A` is a real symmetrix matrix of size, say, n.\n           `k` is the number of Lanczos vectors requested. In typical applications, k << n.\n           `sparse` indicates whether a bare linear function representation of the\n                matrix A is adopted. When it is `true`, the integer parameter `dim`\n                must be supplied giving the actual dimension of square matrix A.\n    Output: A tuple (Qk, T), where Qk = (q1 q2 ... qk) is a n*k matrix, \n            whose columns contain k orthomormal Lanczos vectors q1, q2, ..., qk.\n            I.e., we have Qk^T * Qk = I_k, where I_k is the k-dimensional identity matrix.\n            T is a tridiagonal matrix of size k.\n\n        Theoretically, when input k = n, the corresponding outputs Qn and T satisfy\n    Qn^T * A * Qn = T, and the eigenvalues and eigenvectors of T will be identically\n    the same as that of original matrix A.\n        However, for any k = 1, 2, ..., n, the Lanczos vectors q1, q2, ..., qk are\n    carefully selected in this algorithm that they constitute a orthonormal basis\n    of Krylov space K(A, q1, k) = span{q1, A*q1, ..., A^(k-1)*q1}. Then it can be\n    shown that the eigenvalues in the extreme region(i.e., closed to largest and\n    smallest eigenvalues) and corresponding eigenvectors can be accurately\n    approximated by the results obtained by solving the original eigenvalue problem\n    restricted in the Krylov subspace K(A, q1, k), even though its dimension k\n    (the number of iterations actually performed) is FAR LESS THAN n.\n\n        In practice, after this subroutine is called, one can diagonalize\n    the tridiagonal matrix T to get accurate approximations of eigenvalues of A in\n    the extreme region. The corresponding eigenvectors are obtained by multiplying\n    the "eigenvector representation in the k-dimensional Krylov subspace",\n    which is a k-dimensional vector, by the matrix Qk.\n\n        In practice, the Lanczos iteration turns out to be unstable upon\n    floating point arithmetic. The basic difficulty is caused by loss of orthogonality\n    among the Lanczos vectors, which would mess up the actual result of eigenvectors.\n    In current version, the simple but a bit expensive "full reorthogonalization"\n    approach is adopted to cure this problem.\n    '
    if sparse:
        n = dim
        dtype = torch.float64
        Amap = A
    else:
        n = A.shape[0]
        dtype = A.dtype
        Amap = (lambda v: torch.matmul(A, v))
    Qk = torch.zeros((n, k), dtype=dtype, device=device)
    alphas = torch.zeros(k, dtype=dtype, device=device)
    betas = torch.zeros((k - 1), dtype=dtype, device=device)
    q = torch.randn(n, dtype=dtype, device=device)
    q = (q / torch.norm(q))
    u = Amap(q)
    alpha = torch.matmul(q, u)
    Qk[(:, 0)] = q
    alphas[0] = alpha
    beta = 0
    qprime = torch.randn(n, dtype=dtype, device=device)
    for i in range(1, k):
        r = ((u - (alpha * q)) - (beta * qprime))
        r -= torch.matmul(Qk[(:, :i)], torch.matmul(Qk[(:, :i)].T, r))
        qprime = q
        beta = torch.norm(r)
        q = (r / beta)
        u = Amap(q)
        alpha = torch.matmul(q, u)
        alphas[i] = alpha
        betas[(i - 1)] = beta
        Qk[(:, i)] = q
    T = ((torch.diag(alphas) + torch.diag(betas, diagonal=1)) + torch.diag(betas, diagonal=(- 1)))
    return (Qk, T)
