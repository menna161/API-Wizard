import numpy as np
from skimage.transform import ProjectiveTransform, FundamentalMatrixTransform
from rust_bindings import homogeneous


def homogeneous_matrix(A, b):
    '\n    Example:\n        >>> A = np.array([[1, 2], [3, 4]])\n        >>> b = np.array([5, 6])\n        >>> homogeneous_matrix(A, b)\n        array([[1., 2., 5.],\n               [3., 4., 6.],\n               [0., 0., 1.]])\n    '
    if (A.shape[0] != A.shape[1]):
        raise ValueError("'A' must be a square matrix")
    if (A.shape[0] != b.shape[0]):
        raise ValueError("Number of rows of 'A' must match the number of elements of 'b'")
    d = A.shape[0]
    W = np.identity((d + 1))
    W[(0:d, 0:d)] = A
    W[(0:d, d)] = b
    return W
