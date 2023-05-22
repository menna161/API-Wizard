import pytest
import torch
import numpy as np
from kymatio.scattering1d.backend.torch_backend import backend
from kymatio.scattering1d.backend.torch_skcuda_backend import backend
from skcuda import cublas
import cupy


@pytest.mark.parametrize('backend', backends)
@pytest.mark.parametrize('device', devices)
def test_subsample_fourier(backend, device, random_state=42):
    '\n    Tests whether the periodization in Fourier performs a good subsampling\n    in time\n    '
    if (backend.name.endswith('_skcuda') and (device == 'cpu')):
        with pytest.raises(TypeError) as re:
            x_bad = torch.randn((4, 2)).cpu()
            backend.subsample_fourier(x_bad, 1)
        assert ('for CPU tensors' in re.value.args[0])
        return
    rng = np.random.RandomState(random_state)
    J = 10
    x = (rng.randn(2, 4, (2 ** J)) + (1j * rng.randn(2, 4, (2 ** J))))
    x_f = np.fft.fft(x, axis=(- 1))[(..., np.newaxis)]
    x_f.dtype = 'float64'
    x_f_th = torch.from_numpy(x_f).to(device)
    for j in range((J + 1)):
        x_f_sub_th = backend.subsample_fourier(x_f_th, (2 ** j)).cpu()
        x_f_sub = x_f_sub_th.numpy()
        x_f_sub.dtype = 'complex128'
        x_sub = np.fft.ifft(x_f_sub[(..., 0)], axis=(- 1))
        assert np.allclose(x[(:, :, ::(2 ** j))], x_sub)
    if (device == 'cuda'):
        with pytest.raises(TypeError) as te:
            x_bad = torch.randn(4).cuda()
            backend.subsample_fourier(x_bad, 1)
        assert ('should be complex' in te.value.args[0])
