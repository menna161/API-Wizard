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
def test_fft3d_error(backend, device):
    x = torch.randn(1, 4, 4, 4, 2)
    with pytest.raises(TypeError) as record:
        backend.rfft(x)
    assert ('real' in record.value.args[0])
    x = torch.randn(1, 4, 4, 4, 1)
    with pytest.raises(TypeError) as record:
        backend.ifft(x)
    assert ('complex' in record.value.args[0])
    x = torch.randn(4, 4, 4, 1)
    x = x.to(device)
    y = x[(::2, ::2, ::2)]
    with pytest.raises(RuntimeError) as record:
        backend.rfft(y)
    assert ('must be contiguous' in record.value.args[0])
    x = torch.randn(4, 4, 4, 2)
    x = x.to(device)
    y = x[(::2, ::2, ::2)]
    with pytest.raises(RuntimeError) as record:
        backend.ifft(y)
    assert ('must be contiguous' in record.value.args[0])
