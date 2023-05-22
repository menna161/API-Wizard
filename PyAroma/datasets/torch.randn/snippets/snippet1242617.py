import pytest
import torch
import numpy as np
from kymatio.scattering1d.backend.torch_backend import backend
from kymatio.scattering1d.backend.torch_skcuda_backend import backend
from skcuda import cublas
import cupy


@pytest.mark.parametrize('device', devices)
@pytest.mark.parametrize('backend', backends)
def test_pad_1d(device, backend, random_state=42):
    '\n    Tests the correctness and differentiability of pad_1d\n    '
    torch.manual_seed(random_state)
    N = 128
    for pad_left in range(0, (N - 16), 16):
        for pad_right in [pad_left, (pad_left + 16)]:
            x = torch.randn(2, 4, N, requires_grad=True, device=device)
            x_pad = backend.pad(x, pad_left, pad_right)
            x_pad = x_pad.reshape(x_pad.shape[:(- 1)])
            x2 = x.clone()
            x_pad2 = x_pad.clone()
            for t in range(1, (pad_left + 1)):
                assert torch.allclose(x_pad2[(..., (pad_left - t))], x2[(..., t)])
            for t in range(x.shape[(- 1)]):
                assert torch.allclose(x_pad2[(..., (pad_left + t))], x2[(..., t)])
            for t in range(1, (pad_right + 1)):
                assert torch.allclose(x_pad2[(..., (((x_pad.shape[(- 1)] - 1) - pad_right) + t))], x2[(..., ((x.shape[(- 1)] - 1) - t))])
            for t in range(1, (pad_right + 1)):
                assert torch.allclose(x_pad2[(..., (((x_pad.shape[(- 1)] - 1) - pad_right) - t))], x2[(..., ((x.shape[(- 1)] - 1) - t))])
            loss = (0.5 * torch.sum((x_pad ** 2)))
            loss.backward()
            x_grad_original = x.clone()
            x_grad = x_grad_original.new(x_grad_original.shape).fill_(0.0)
            x_grad += x_grad_original
            for t in range(1, (pad_left + 1)):
                x_grad[(..., t)] += x_grad_original[(..., t)]
            for t in range(1, (pad_right + 1)):
                t0 = ((x.shape[(- 1)] - 1) - t)
                x_grad[(..., t0)] += x_grad_original[(..., t0)]
            assert torch.allclose(x.grad, x_grad)
    with pytest.raises(ValueError) as ve:
        backend.pad(x, x.shape[(- 1)], 0)
    assert ('padding size' in ve.value.args[0])
    with pytest.raises(ValueError) as ve:
        backend.pad(x, 0, x.shape[(- 1)])
    assert ('padding size' in ve.value.args[0])
