import numpy as np
import torch
import pytest
from collections import namedtuple
from kymatio.scattering2d.backend.torch_backend import backend
from kymatio.scattering2d.backend.torch_skcuda_backend import backend
from skcuda import cublas
import cupy
import numpy as np


@pytest.mark.parametrize('backend', backends)
def test_stack(self, backend):
    x = torch.randn(3, 6, 6)
    y = torch.randn(3, 6, 6)
    z = torch.randn(3, 6, 6)
    w = backend.stack((x, y, z))
    assert (w.shape == (((x.shape[0],) + (3,)) + x.shape[(- 2):]))
    assert np.allclose(w[(:, 0, ...)], x)
    assert np.allclose(w[(:, 1, ...)], y)
    assert np.allclose(w[(:, 2, ...)], z)
