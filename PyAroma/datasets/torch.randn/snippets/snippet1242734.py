import torch
from kymatio.torch import Scattering1D
from kymatio.scattering1d.backend.torch_backend import backend
from kymatio.scattering1d.backend.torch_skcuda_backend import backend
from skcuda import cublas
import cupy


def setup(self, sc_params, backend, device):
    n_channels = 1
    scattering = Scattering1D(backend=backend, J=sc_params['J'], shape=sc_params['shape'], Q=sc_params['Q'])
    bs = sc_params['batch_size']
    x = torch.randn(bs, n_channels, sc_params['shape']).float().to(device)
    self.scattering = scattering.to(device)
    self.x = x.to(device)
    y = self.scattering(self.x)
