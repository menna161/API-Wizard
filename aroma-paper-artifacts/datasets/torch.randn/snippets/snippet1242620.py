import pytest
import torch
import numpy as np
from kymatio.scattering1d.backend.torch_backend import backend
from kymatio.scattering1d.backend.torch_skcuda_backend import backend
from skcuda import cublas
import cupy


@pytest.mark.parametrize('backend', backends)
@pytest.mark.parametrize('device', devices)
def test_unpad(backend, device):
    if ((backend.name == 'torch_skcuda') and (device == 'cpu')):
        pytest.skip()
    x = torch.randn(8, 4, 1).to(device)
    y = backend.unpad(x, 1, 3)
    assert (y.shape == (8, 2))
    assert torch.allclose(y, x[(:, 1:3, 0)])
    N = 128
    x = torch.rand(2, 4, N).to(device)
    for pad_left in range(0, (N - 16), 16):
        pad_right = (pad_left + 16)
        x_pad = backend.pad(x, pad_left, pad_right)
        x_unpadded = backend.unpad(x_pad, pad_left, ((x_pad.shape[(- 1)] - pad_right) - 1))
        assert torch.allclose(x, x_unpadded)
