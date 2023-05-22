from kymatio.torch import Scattering2D
import torch
from kymatio.scattering2d.backend.torch_backend import backend
from kymatio.scattering2d.backend.torch_skcuda_backend import backend
from skcuda import cublas
import cupy


def setup(self, sc_params, backend, device):
    n_channels = 3
    scattering = Scattering2D(backend=backend, J=sc_params['J'], shape=sc_params['shape'], L=sc_params['L'])
    bs = sc_params['batch_size']
    x = torch.randn(bs, n_channels, sc_params['shape'][0], sc_params['shape'][1]).float().to(device)
    self.scattering = scattering.to(device)
    self.x = x.to(device)
    y = self.scattering(self.x)
