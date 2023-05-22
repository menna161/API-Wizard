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
def test_larger_scales(device, backend):
    if (backend.name.endswith('_skcuda') and (device == 'cpu')):
        pytest.skip('The skcuda backend does not support CPU tensors.')
    shape = (32, 32, 32)
    L = 3
    sigma_0 = 1
    x = torch.randn(((1,) + shape)).to(device)
    for J in range(3, (4 + 1)):
        scattering = HarmonicScattering3D(J=J, shape=shape, L=L, sigma_0=sigma_0, backend=backend).to(device)
        scattering.method = 'integral'
        Sx = scattering(x)
