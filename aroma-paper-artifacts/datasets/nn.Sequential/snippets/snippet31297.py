import torch
import torch.nn as nn
import torch.nn.functional as F
from .modules import spectral_norm


def __init__(self, outer_nc, inner_nc, input_nc, submodule=None, outermost=False, innermost=False, norm_layer=nn.BatchNorm2d, use_spectral_norm=False):
    super(UnetSkipConnectionBlock, self).__init__()
    self.outermost = outermost
    if (input_nc is None):
        input_nc = outer_nc
    downconv = spectral_norm(nn.Conv2d(input_nc, inner_nc, kernel_size=4, stride=2, padding=1), use_spectral_norm)
    downrelu = nn.LeakyReLU(0.2, True)
    downnorm = norm_layer(inner_nc)
    uprelu = nn.ReLU(True)
    upnorm = norm_layer(outer_nc)
    if outermost:
        upconv = spectral_norm(nn.ConvTranspose2d((inner_nc * 2), outer_nc, kernel_size=4, stride=2, padding=1), use_spectral_norm)
        down = [downconv]
        up = [uprelu, upconv, nn.Tanh()]
        model = ((down + [submodule]) + up)
    elif innermost:
        upconv = spectral_norm(nn.ConvTranspose2d(inner_nc, outer_nc, kernel_size=4, stride=2, padding=1), use_spectral_norm)
        down = [downrelu, downconv]
        up = [uprelu, upconv, upnorm]
        model = (down + up)
    else:
        upconv = spectral_norm(nn.ConvTranspose2d((inner_nc * 2), outer_nc, kernel_size=4, stride=2, padding=1), use_spectral_norm)
        down = [downrelu, downconv, downnorm]
        up = [uprelu, upconv, upnorm]
        model = ((down + [submodule]) + up)
    self.model = nn.Sequential(*model)
