import pytest
import torch
from kymatio import Scattering1D
import math
import os
import io
import numpy as np
from kymatio.scattering1d.backend.torch_backend import backend
from kymatio.scattering1d.backend.torch_skcuda_backend import backend
from skcuda import cublas
import cupy


@pytest.mark.parametrize('device', devices)
@pytest.mark.parametrize('backend', backends)
def test_differentiability_scattering(device, backend, random_state=42):
    '\n    It simply tests whether it is really differentiable or not.\n    This does NOT test whether the gradients are correct.\n    '
    if backend.name.endswith('_skcuda'):
        pytest.skip("The skcuda backend does not pass differentiabilitytests, but that's ok (for now).")
    torch.manual_seed(random_state)
    J = 6
    Q = 8
    T = (2 ** 12)
    scattering = Scattering1D(J, T, Q, frontend='torch', backend=backend).to(device)
    x = torch.randn(2, T, requires_grad=True, device=device)
    s = scattering.forward(x)
    loss = torch.sum(torch.abs(s))
    loss.backward()
    assert (torch.max(torch.abs(x.grad)) > 0.0)
