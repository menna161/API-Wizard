import numpy as np
from .topology import cellular_automaton2d


def _get_boundary_indices(self, shape):
    m = np.arange((shape[0] * shape[1])).reshape(shape)
    return np.concatenate((m[0], m[(- 1)], m[(:, 0)], m[(:, (- 1))]), axis=None)
