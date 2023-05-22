import torch
import torch.nn as nn
import torch.utils.model_zoo as model_zoo
import torch.nn.functional as F


def __init__(self, base_inplanes, base_planes, stride):
    super(first_conv_block, self).__init__()
    max_inp = base_inplanes
    max_oup = base_planes
    self.max_inp = max_inp
    self.max_oup = max_oup
    self.stride = stride
    self.fc11 = nn.Linear(1, 32)
    self.fc12 = nn.Linear(32, (((self.max_oup * self.max_inp) * 7) * 7))
    self.first_bn = nn.ModuleList()
    for oup_scale in channel_scale:
        oup = int((self.max_oup * oup_scale))
        self.first_bn.append(nn.BatchNorm2d(oup, affine=False))
    self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)
