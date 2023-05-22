import numpy as np
import pytest
import torch, tensorflow as tf
import jax.numpy as jnp
from jax import device_put
import kymatio
from kymatio import TimeFrequencyScattering
from kymatio.scattering1d.core.scattering1d import scattering1d
from kymatio.scattering1d.filter_bank import gauss_1d
from kymatio.scattering1d.core.timefrequency_scattering import joint_timefrequency_scattering, time_scattering_widthfirst, frequency_scattering, time_averaging, frequency_averaging
from kymatio.scattering1d.frontend.base_frontend import TimeFrequencyScatteringBase
from kymatio.scattering1d.frontend.torch_frontend import TimeFrequencyScatteringTorch
from kymatio.scattering1d.frontend.numpy_frontend import TimeFrequencyScatteringNumPy
from kymatio.jax import TimeFrequencyScattering as TimeFrequencyScatteringJax


def test_differentiability_jtfs_torch(random_state=42):
    device = 'cpu'
    J = 8
    J_fr = 3
    shape = (4096,)
    Q = 8
    S = TimeFrequencyScatteringTorch(J=J, J_fr=J_fr, shape=shape, Q=Q, T=0, F=0).to(device)
    S.build()
    S.create_filters()
    S.load_filters()
    backend = S.backend
    torch.manual_seed(random_state)
    x = torch.randn(shape, requires_grad=True, device=device)
    x_shape = backend.shape(x)
    (_, signal_shape) = (x_shape[:(- 1)], x_shape[(- 1):])
    x_reshaped = backend.reshape_input(x, signal_shape)
    U_0_in = backend.pad(x_reshaped, pad_left=S.pad_left, pad_right=S.pad_right)
    filters = [S.phi_f, S.psi1_f, S.psi2_f]
    jtfs_gen = joint_timefrequency_scattering(U_0_in, backend, filters, S.log2_stride, (S.average == 'local'), S.filters_fr, S.log2_stride_fr, (S.average_fr == 'local'))
    S_0 = next(jtfs_gen)
    loss = torch.linalg.norm(S_0['coef'])
    loss.backward(retain_graph=True)
    assert (torch.abs(loss) >= 0.0)
    grad = x.grad
    assert (torch.max(torch.abs(grad)) > 0.0)
    for S in jtfs_gen:
        loss = torch.linalg.norm(S['coef'])
        loss.backward(retain_graph=True)
        assert (torch.abs(loss) >= 0.0)
        grad = x.grad
        assert (torch.max(torch.abs(grad)) > 0.0)
