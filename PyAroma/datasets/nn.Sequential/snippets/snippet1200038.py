import torch
import torch.nn as nn
from torch.nn import init
import functools
from torch.optim import lr_scheduler
from deeplab import Deeplab
from collections import OrderedDict
import torch.nn.functional as F
from fcn8s_LSD import FCN8s_LSD


def __init__(self, input_nc, output_nc, ngf=64, norm_layer=nn.BatchNorm2d, use_dropout=False, n_blocks=6, padding_type='reflect'):
    assert (n_blocks >= 0)
    super(ResnetGenerator, self).__init__()
    self.input_nc = input_nc
    self.output_nc = output_nc
    self.ngf = ngf
    if (type(norm_layer) == functools.partial):
        use_bias = (norm_layer.func == nn.InstanceNorm2d)
    else:
        use_bias = (norm_layer == nn.InstanceNorm2d)
    model = [nn.ReflectionPad2d(3), nn.Conv2d(input_nc, ngf, kernel_size=7, padding=0, bias=use_bias), norm_layer(ngf), nn.ReLU(True)]
    n_downsampling = 2
    for i in range(n_downsampling):
        mult = (2 ** i)
        model += [nn.Conv2d((ngf * mult), ((ngf * mult) * 2), kernel_size=3, stride=2, padding=1, bias=use_bias), norm_layer(((ngf * mult) * 2)), nn.ReLU(True)]
    mult = (2 ** n_downsampling)
    for i in range(n_blocks):
        model += [ResnetBlock((ngf * mult), padding_type=padding_type, norm_layer=norm_layer, use_dropout=use_dropout, use_bias=use_bias)]
    for i in range(n_downsampling):
        mult = (2 ** (n_downsampling - i))
        model += [nn.ConvTranspose2d((ngf * mult), int(((ngf * mult) / 2)), kernel_size=3, stride=2, padding=1, output_padding=1, bias=use_bias), norm_layer(int(((ngf * mult) / 2))), nn.ReLU(True)]
    model += [nn.ReflectionPad2d(3)]
    model += [nn.Conv2d(ngf, output_nc, kernel_size=7, padding=0)]
    model += [nn.Tanh()]
    self.model = nn.Sequential(*model)
