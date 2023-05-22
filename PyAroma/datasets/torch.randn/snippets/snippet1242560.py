import torch
import pytest
from kymatio.backend.torch_backend import ModulusStable, TorchBackend


def test_reshape():
    backend = TorchBackend
    x = torch.randn(3, 5, 16)
    y = backend.reshape_input(x, signal_shape=(16,))
    xbis = backend.reshape_output(y, batch_shape=(3, 5), n_kept_dims=1)
    assert (backend.shape(x) == x.shape)
    assert (y.shape == (15, 1, 16))
    assert torch.allclose(x, xbis)
    x = torch.randn(3, 5, 16, 16)
    y = backend.reshape_input(x, signal_shape=(16, 16))
    xbis = backend.reshape_output(y, batch_shape=(3, 5), n_kept_dims=2)
    assert (backend.shape(x) == x.shape)
    assert (y.shape == (15, 1, 16, 16))
    assert torch.allclose(x, xbis)
    x = torch.randn(3, 5, 16, 16, 16)
    y = backend.reshape_input(x, signal_shape=(16, 16, 16))
    xbis = backend.reshape_output(y, batch_shape=(3, 5), n_kept_dims=3)
    assert (backend.shape(x) == x.shape)
    assert (y.shape == (15, 1, 16, 16, 16))
    assert torch.allclose(x, xbis)
