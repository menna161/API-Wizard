import torch
import os
import io
import numpy as np
import pytest
from kymatio.torch import HarmonicScattering3D
from kymatio.scattering3d.utils import generate_weighted_sum_of_gaussians
from kymatio.scattering3d.backend.torch_backend import backend
from kymatio.scattering3d.backend.torch_skcuda_backend import backend
from skcuda import cublas
import cupy


@pytest.mark.parametrize('device', devices)
@pytest.mark.parametrize('backend', backends)
def test_complex_modulus(backend, device):
    if ((backend.name == 'torch_skcuda') and (device == 'cpu')):
        pytest.skip('The skcuda backend does not support CPU tensors.')
    x = torch.randn(4, 3, 2).to(device)
    xm = torch.sqrt(((x[(..., 0)] ** 2) + (x[(..., 1)] ** 2)))
    y = backend.modulus(x)
    y = y.reshape(y.shape[:(- 1)])
    assert ((y - xm).norm() < 1e-07)
