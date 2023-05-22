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
def test_fft_exceptions(self, backend_device):
    (backend, device) = backend_device
    x = torch.randn(4, 4, 2)
    x = x.to(device)
    with pytest.raises(TypeError) as record:
        backend.rfft(x)
    assert ('real' in record.value.args[0])
    x = torch.randn(4, 4, 1)
    x = x.to(device)
    with pytest.raises(TypeError) as record:
        backend.ifft(x)
    assert ('complex' in record.value.args[0])
    x = torch.randn(4, 4, 1)
    x = x.to(device)
    with pytest.raises(TypeError) as record:
        backend.irfft(x)
    assert ('complex' in record.value.args[0])
    x = torch.randn(4, 4, 1)
    x = x.to(device)
    y = x[(::2, ::2)]
    with pytest.raises(RuntimeError) as record:
        backend.rfft(y)
    assert ('must be contiguous' in record.value.args[0])
    x = torch.randn(4, 4, 2)
    x = x.to(device)
    y = x[(::2, ::2)]
    with pytest.raises(RuntimeError) as record:
        backend.ifft(y)
    assert ('must be contiguous' in record.value.args[0])
    x = torch.randn(4, 4, 2)
    x = x.to(device)
    y = x[(::2, ::2)]
    with pytest.raises(RuntimeError) as record:
        backend.irfft(y)
    assert ('must be contiguous' in record.value.args[0])
