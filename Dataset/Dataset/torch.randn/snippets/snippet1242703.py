import os
import io
import numpy as np
import torch
import pytest
from kymatio import Scattering2D
from torch.autograd import gradcheck
from collections import namedtuple
from kymatio.scattering2d.backend.torch_backend import backend
from kymatio.scattering2d.backend.torch_skcuda_backend import backend
from skcuda import cublas
import cupy


@pytest.mark.parametrize('backend_device', backends_devices)
def test_scattering2d_errors(self, backend_device):
    (backend, device) = backend_device
    S = Scattering2D(3, (32, 32), backend=backend, frontend='torch')
    S.to(device)
    with pytest.raises(TypeError) as record:
        S(None)
    assert ('input should be' in record.value.args[0])
    x = torch.randn(4, 4)
    y = x[(::2, ::2)]
    with pytest.raises(RuntimeError) as record:
        S(y)
    assert ('must be contiguous' in record.value.args[0])
    x = torch.randn(31, 31)
    with pytest.raises(RuntimeError) as record:
        S(x)
    assert ('Tensor must be of spatial size' in record.value.args[0])
    S = Scattering2D(3, (32, 32), pre_pad=True, backend=backend, frontend='torch')
    with pytest.raises(RuntimeError) as record:
        S(x)
    assert ('Padded tensor must be of spatial size' in record.value.args[0])
    x = torch.randn(8, 8)
    S = Scattering2D(2, (8, 8), backend=backend, frontend='torch')
    x = x.to(device)
    S = S.to(device)
    if (not ((device == 'cpu') and (backend.name == 'torch_skcuda'))):
        y = S(x)
        assert (x.device == y.device)
