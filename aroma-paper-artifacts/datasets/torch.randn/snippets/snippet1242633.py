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
def test_output_size(device, backend, random_state=42):
    '\n    Tests that S.output_size() returns the same size as S.scattering(x)\n    '
    torch.manual_seed(random_state)
    J = 6
    Q = 8
    N = (2 ** 12)
    scattering = Scattering1D(J, N, Q, out_type='dict', backend=backend, frontend='torch')
    x = torch.randn(2, N)
    scattering.to(device)
    x = x.to(device)
    if ((not backend.name.endswith('_skcuda')) or (device != 'cpu')):
        for max_order in [1, 2]:
            scattering.max_order = max_order
            s_dico = scattering(x)
            for detail in [True, False]:
                size = scattering.output_size(detail=detail)
                if detail:
                    num_orders = {0: 0, 1: 0, 2: 0}
                    for k in s_dico.keys():
                        if (k == ()):
                            num_orders[0] += 1
                        elif (len(k) == 1):
                            num_orders[1] += 1
                        elif (len(k) == 2):
                            num_orders[2] += 1
                    todo = (2 if (max_order == 2) else 1)
                    for i in range(todo):
                        assert (num_orders[i] == size[i])
                else:
                    assert (len(s_dico) == size)
