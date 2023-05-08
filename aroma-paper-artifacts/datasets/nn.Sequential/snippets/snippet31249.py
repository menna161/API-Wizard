import functools
import torch.nn as nn
from .denset_net import *
from .modules import *


def __init__(self, input_nc, ndf=64, n_layers=3, norm_layer=nn.BatchNorm2d, use_sigmoid=False, use_spectral_norm=True):
    super(NLayerDiscriminator, self).__init__()
    if (type(norm_layer) == functools.partial):
        use_bias = (norm_layer.func == nn.InstanceNorm2d)
    else:
        use_bias = (norm_layer == nn.InstanceNorm2d)
    kw = 4
    padw = 1
    sequence = [spectral_norm(nn.Conv2d(input_nc, ndf, kernel_size=kw, stride=2, padding=padw), use_spectral_norm), nn.LeakyReLU(0.2, True)]
    nf_mult = 1
    nf_mult_prev = 1
    for n in range(1, n_layers):
        nf_mult_prev = nf_mult
        nf_mult = min((2 ** n), 8)
        sequence += [spectral_norm(nn.Conv2d((ndf * nf_mult_prev), (ndf * nf_mult), kernel_size=kw, stride=2, padding=padw, bias=use_bias), use_spectral_norm), norm_layer((ndf * nf_mult)), nn.LeakyReLU(0.2, True)]
    nf_mult_prev = nf_mult
    nf_mult = min((2 ** n_layers), 8)
    sequence += [spectral_norm(nn.Conv2d((ndf * nf_mult_prev), (ndf * nf_mult), kernel_size=kw, stride=1, padding=padw, bias=use_bias), use_spectral_norm), norm_layer((ndf * nf_mult)), nn.LeakyReLU(0.2, True)]
    sequence += [spectral_norm(nn.Conv2d((ndf * nf_mult), 1, kernel_size=kw, stride=1, padding=padw), use_spectral_norm)]
    if use_sigmoid:
        sequence += [nn.Sigmoid()]
    self.model = nn.Sequential(*sequence)
