import numpy as np
from .. import _base


def normalize(self):
    'Normalize the rotation matrix to ensure it is valid and\n        negate the effect of rounding errors.\n        '
    (U, _, V) = np.linalg.svd(self.mat, full_matrices=False)
    S = np.identity(self.dim)
    S[((self.dim - 1), (self.dim - 1))] = (np.linalg.det(U) * np.linalg.det(V))
    self.mat = U.dot(S).dot(V)
