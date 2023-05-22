from kymatio.torch import HarmonicScattering3D
import torch
from kymatio.scattering3d.backend.torch_backend import backend
from kymatio.scattering3d.backend.torch_skcuda_backend import backend
from skcuda import cublas
import cupy


def setup(self, sc_params, backend, device):
    scattering = HarmonicScattering3D(backend=backend, J=sc_params['J'], shape=sc_params['shape'], L=sc_params['L'])
    bs = sc_params['batch_size']
    x = torch.randn(bs, sc_params['shape'][0], sc_params['shape'][1], sc_params['shape'][2]).float()
    self.scattering = scattering.to(device)
    self.x = x.to(device)
