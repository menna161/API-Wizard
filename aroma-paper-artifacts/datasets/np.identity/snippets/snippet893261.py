import numpy as np
from .. import _base


@classmethod
def is_valid_matrix(cls, mat):
    'Check if a matrix is a valid rotation matrix.'
    return ((mat.shape == (cls.dim, cls.dim)) and np.isclose(np.linalg.det(mat), 1.0) and np.allclose(mat.T.dot(mat), np.identity(cls.dim)))
