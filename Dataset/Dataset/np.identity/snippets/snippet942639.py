import numpy as np
from scipy.spatial.transform import Rotation


def is_rotation_matrix(R):
    assert (R.shape[0] == R.shape[1])
    I = np.identity(3)
    return (np.isclose(np.dot(R, R.T), I).all() and np.isclose(np.linalg.det(R), 1.0))
