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


@pytest.mark.parametrize('backend', backends)
def test_scattering_GPU_CPU(backend, random_state=42):
    '\n    This function tests whether the CPU computations are equivalent to\n    the GPU ones\n    '
    if (torch.cuda.is_available() and (not backend.name.endswith('_skcuda'))):
        torch.manual_seed(random_state)
        J = 6
        Q = 8
        T = (2 ** 12)
        scattering = Scattering1D(J, T, Q, backend=backend, frontend='torch').cpu()
        x = torch.randn(2, T)
        s_cpu = scattering(x)
        scattering = scattering.cuda()
        x_gpu = x.clone().cuda()
        s_gpu = scattering(x_gpu).cpu()
        Warning('Tolerance has been slightly lowered here...')
        assert torch.allclose(s_cpu, s_gpu, atol=1e-07)
