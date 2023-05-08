import torch
import torch.nn as nn
import torch.nn.functional as F
from models.shift_net.InnerShiftTriple import InnerShiftTriple
from models.shift_net.InnerCos import InnerCos
from models.face_shift_net.InnerFaceShiftTriple import InnerFaceShiftTriple
from models.res_shift_net.innerResShiftTriple import InnerResShiftTriple
from models.patch_soft_shift.innerPatchSoftShiftTriple import InnerPatchSoftShiftTriple
from models.res_patch_soft_shift.innerResPatchSoftShiftTriple import InnerResPatchSoftShiftTriple
from .unet import UnetSkipConnectionBlock
from .modules import *


def __init__(self, outer_nc, inner_nc, opt, innerCos_list, shift_list, mask_global, input_nc, submodule=None, shift_layer=None, outermost=False, innermost=False, norm_layer=nn.BatchNorm2d, use_spectral_norm=False, layer_to_last=3):
    super(UnetSkipConnectionShiftBlock, self).__init__()
    self.outermost = outermost
    if (input_nc is None):
        input_nc = outer_nc
    downconv = spectral_norm(nn.Conv2d(input_nc, inner_nc, kernel_size=4, stride=2, padding=1), use_spectral_norm)
    downrelu = nn.LeakyReLU(0.2, True)
    downnorm = norm_layer(inner_nc)
    uprelu = nn.ReLU(True)
    upnorm = norm_layer(outer_nc)
    device = ('cpu' if (len(opt.gpu_ids) == 0) else 'gpu')
    shift = InnerShiftTriple(opt.shift_sz, opt.stride, opt.mask_thred, opt.triple_weight, layer_to_last=layer_to_last, device=device)
    shift.set_mask(mask_global)
    shift_list.append(shift)
    innerCos = InnerCos(strength=opt.strength, skip=opt.skip, layer_to_last=layer_to_last, device=device)
    innerCos.set_mask(mask_global)
    innerCos_list.append(innerCos)
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
        upconv = spectral_norm(nn.ConvTranspose2d((inner_nc * 3), outer_nc, kernel_size=4, stride=2, padding=1), use_spectral_norm)
        down = [downrelu, downconv, downnorm]
        up = [uprelu, innerCos, shift, upconv, upnorm]
        model = ((down + [submodule]) + up)
    self.model = nn.Sequential(*model)
