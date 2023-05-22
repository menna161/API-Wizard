import pytest
import torch
import numpy as np
from kymatio.scattering1d.backend.torch_backend import backend
from kymatio.scattering1d.backend.torch_skcuda_backend import backend
from skcuda import cublas
import cupy


@pytest.mark.parametrize('device', devices)
@pytest.mark.parametrize('backend', backends)
def test_modulus(device, backend, random_state=42):
    '\n    Tests the stability and differentiability of modulus\n    '
    if (backend.name.endswith('_skcuda') and (device == 'cpu')):
        with pytest.raises(TypeError) as re:
            x_bad = torch.randn((4, 2)).cpu()
            backend.modulus(x_bad)
        assert ('for CPU tensors' in re.value.args[0])
        return
    torch.manual_seed(random_state)
    x = torch.randn(2, 4, 128, 2, requires_grad=True, device=device)
    x_abs = backend.modulus(x).squeeze((- 1))
    assert (len(x_abs.shape) == len(x.shape[:(- 1)]))
    x_abs2 = x_abs.clone()
    x2 = x.clone()
    assert torch.allclose(x_abs2, torch.sqrt(((x2[(..., 0)] ** 2) + (x2[(..., 1)] ** 2))))
    with pytest.raises(TypeError) as te:
        x_bad = torch.randn(4).to(device)
        backend.modulus(x_bad)
    assert ('should be complex' in te.value.args[0])
    if backend.name.endswith('_skcuda'):
        pytest.skip("The skcuda backend does not pass differentiabilitytests, but that's ok (for now).")
    loss = torch.sum(x_abs)
    loss.backward()
    x_grad = (x2 / x_abs2[(..., None)])
    assert torch.allclose(x.grad, x_grad)
    x0 = torch.zeros(100, 4, 128, 2, requires_grad=True, device=device)
    x_abs0 = backend.modulus(x0)
    loss0 = torch.sum(x_abs0)
    loss0.backward()
    assert (torch.max(torch.abs(x0.grad)) <= 1e-07)
