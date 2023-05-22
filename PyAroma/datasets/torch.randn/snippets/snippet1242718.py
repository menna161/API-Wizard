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
def test_cdgmm3d(device, backend):
    if ((not backend.name.endswith('_skcuda')) or (device != 'cpu')):
        x = torch.zeros(2, 3, 4, 2).to(device)
        x[(..., 0)] = 2
        x[(..., 1)] = 3
        y = torch.zeros_like(x)
        y[(..., 0)] = 4
        y[(..., 1)] = 5
        prod = torch.zeros_like(x)
        prod[(..., 0)] = ((x[(..., 0)] * y[(..., 0)]) - (x[(..., 1)] * y[(..., 1)]))
        prod[(..., 1)] = ((x[(..., 0)] * y[(..., 1)]) + (x[(..., 1)] * y[(..., 0)]))
        z = backend.cdgmm3d(x, y)
        assert ((z - prod).norm().cpu().item() < 1e-07)
        with pytest.raises(RuntimeError) as record:
            x = torch.randn((3, 4, 3, 2), device=device)
            x = x[(:, 0:3, ...)]
            y = torch.randn((3, 3, 3, 2), device=device)
            backend.cdgmm3d(x, y)
        assert ('contiguous' in record.value.args[0])
        with pytest.raises(RuntimeError) as record:
            x = torch.randn((3, 3, 3, 2), device=device)
            y = torch.randn((3, 4, 3, 2), device=device)
            y = y[(:, 0:3, ...)]
            backend.cdgmm3d(x, y)
        assert ('contiguous' in record.value.args[0])
        with pytest.raises(RuntimeError) as record:
            x = torch.randn((3, 3, 3, 2), device=device)
            y = torch.randn((4, 4, 4, 2), device=device)
            backend.cdgmm3d(x, y)
        assert ('not compatible' in record.value.args[0])
        with pytest.raises(TypeError) as record:
            x = torch.randn(3, 3, 3, 2).double()
            y = torch.randn(3, 3, 3, 2)
            backend.cdgmm3d(x, y)
        assert (' must be of the same dtype' in record.value.args[0])
    if backend.name.endswith('_skcuda'):
        x = torch.randn((3, 3, 3, 2), device=torch.device('cpu'))
        y = torch.randn((3, 3, 3, 2), device=torch.device('cpu'))
        with pytest.raises(TypeError) as record:
            backend.cdgmm3d(x, y)
        assert ('must be CUDA' in record.value.args[0])
