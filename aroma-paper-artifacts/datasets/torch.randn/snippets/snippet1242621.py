import pytest
import torch
import numpy as np
from kymatio.scattering1d.backend.torch_backend import backend
from kymatio.scattering1d.backend.torch_skcuda_backend import backend
from skcuda import cublas
import cupy


@pytest.mark.parametrize('backend', backends)
@pytest.mark.parametrize('device', devices)
def test_fft_type(backend, device):
    if ((backend.name == 'torch_skcuda') and (device == 'cpu')):
        pytest.skip()
    x = torch.randn(8, 4, 2).to(device)
    with pytest.raises(TypeError) as record:
        y = backend.rfft(x)
    assert ('should be real' in record.value.args[0])
    x = torch.randn(8, 4, 1).to(device)
    with pytest.raises(TypeError) as record:
        y = backend.ifft(x)
    assert ('should be complex' in record.value.args[0])
    with pytest.raises(TypeError) as record:
        y = backend.irfft(x)
    assert ('should be complex' in record.value.args[0])
