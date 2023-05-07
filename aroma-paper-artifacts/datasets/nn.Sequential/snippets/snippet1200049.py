import torch
import torch.nn as nn
from torch.nn import init
import functools
from torch.optim import lr_scheduler
from deeplab import Deeplab
from collections import OrderedDict
import torch.nn.functional as F
from fcn8s_LSD import FCN8s_LSD


def __init__(self, input_nc, ndf=64, norm_layer=nn.BatchNorm2d, use_sigmoid=False):
    super(PixelDiscriminator, self).__init__()
    if (type(norm_layer) == functools.partial):
        use_bias = (norm_layer.func == nn.InstanceNorm2d)
    else:
        use_bias = (norm_layer == nn.InstanceNorm2d)
    self.net = [nn.Conv2d(input_nc, ndf, kernel_size=1, stride=1, padding=0), nn.LeakyReLU(0.2, True), nn.Conv2d(ndf, (ndf * 2), kernel_size=1, stride=1, padding=0, bias=use_bias), norm_layer((ndf * 2)), nn.LeakyReLU(0.2, True), nn.Conv2d((ndf * 2), 1, kernel_size=1, stride=1, padding=0, bias=use_bias)]
    if use_sigmoid:
        self.net.append(nn.Sigmoid())
    self.net = nn.Sequential(*self.net)
