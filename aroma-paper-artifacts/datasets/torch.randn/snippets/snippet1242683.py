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
def test_Pad(self, backend_device):
    (backend, device) = backend_device
    pad = backend.Pad((2, 2, 2, 2), (4, 4))
    x = torch.randn(1, 4, 4)
    x = x.to(device)
    z = pad(x)
    assert (z.shape == (1, 8, 8, 1))
    assert torch.allclose(z[(0, 2, 2)], x[(0, 0, 0)])
    assert torch.allclose(z[(0, 1, 0)], x[(0, 1, 2)])
    assert torch.allclose(z[(0, 1, 1)], x[(0, 1, 1)])
    assert torch.allclose(z[(0, 1, 2)], x[(0, 1, 0)])
    assert torch.allclose(z[(0, 1, 3)], x[(0, 1, 1)])
