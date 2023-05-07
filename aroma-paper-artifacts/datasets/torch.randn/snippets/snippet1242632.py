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
def test_coordinates(device, backend, random_state=42):
    '\n    Tests whether the coordinates correspond to the actual values (obtained\n    with Scattering1d.meta()), and with the vectorization\n    '
    torch.manual_seed(random_state)
    J = 6
    Q = 8
    T = (2 ** 12)
    scattering = Scattering1D(J, T, Q, max_order=2, backend=backend, frontend='torch')
    x = torch.randn(2, T)
    scattering.to(device)
    x = x.to(device)
    for max_order in [1, 2]:
        scattering.max_order = max_order
        scattering.out_type = 'dict'
        if (backend.name.endswith('skcuda') and (device == 'cpu')):
            with pytest.raises(TypeError) as ve:
                s_dico = scattering(x)
            assert ('CUDA' in ve.value.args[0])
        else:
            s_dico = scattering(x)
            s_dico = {k: s_dico[k].data for k in s_dico.keys()}
        scattering.out_type = 'array'
        if (backend.name.endswith('_skcuda') and (device == 'cpu')):
            with pytest.raises(TypeError) as ve:
                s_vec = scattering(x)
            assert ('CUDA' in ve.value.args[0])
        else:
            s_vec = scattering(x)
            s_dico = {k: s_dico[k].cpu() for k in s_dico.keys()}
            s_vec = s_vec.cpu()
        meta = scattering.meta()
        if ((not backend.name.endswith('_skcuda')) or (device != 'cpu')):
            assert (len(s_dico) == s_vec.shape[1])
            for cc in range(s_vec.shape[1]):
                k = meta['key'][cc]
                assert torch.allclose(s_vec[(:, cc)], torch.squeeze(s_dico[k]))
