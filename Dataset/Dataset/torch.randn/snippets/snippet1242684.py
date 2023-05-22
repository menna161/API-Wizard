import numpy as np
import torch
import pytest
from collections import namedtuple
from kymatio.scattering2d.backend.torch_backend import backend
from kymatio.scattering2d.backend.torch_skcuda_backend import backend
from skcuda import cublas
import cupy
import numpy as np


@pytest.mark.parametrize('backend_device', backends_devices)
def test_unpad(self, backend_device):
    (backend, device) = backend_device
    x = torch.randn(4, 4, 1)
    x = x.to(device)
    y = backend.unpad(x)
    assert (y.shape == (2, 2))
    assert torch.allclose(y[(0, 0)], x[(1, 1, 0)])
    assert torch.allclose(y[(0, 1)], x[(1, 2, 0)])
