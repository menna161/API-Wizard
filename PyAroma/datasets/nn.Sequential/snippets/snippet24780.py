import torch
import torch.nn as nn


def __init__(self, inplanes, block, planes, blocks, stride=1, dilate=False):
    super(ResidualStage, self).__init__()
    self.dim = (planes * block.expansion)
    self.n = blocks
    norm_layer = nn.BatchNorm2d
    self.downsample = None
    self.inplanes = inplanes
    self.groups = 1
    self.base_width = 64
    previous_dilation = 1
    self.dilation = 1
    self.relu = nn.ReLU(inplace=True)
    if dilate:
        self.dilation *= stride
        stride = 1
    self.block_1 = block(self.inplanes, planes, stride, self.groups, self.base_width, previous_dilation, norm_layer)
    if ((stride != 1) or (self.inplanes != (planes * block.expansion))):
        self.downsample = nn.Sequential(conv1x1(self.inplanes, (planes * block.expansion), stride), norm_layer((planes * block.expansion)))
    self.inplanes = (planes * block.expansion)
    self.block_2 = block(self.inplanes, planes, groups=self.groups, base_width=self.base_width, dilation=self.dilation, norm_layer=norm_layer)
    self.block_3 = block(self.inplanes, planes, groups=self.groups, base_width=self.base_width, dilation=self.dilation, norm_layer=norm_layer)
    if (self.n > 3):
        self.block_4 = block(self.inplanes, planes, groups=self.groups, base_width=self.base_width, dilation=self.dilation, norm_layer=norm_layer)
    if (self.n > 4):
        self.block_5 = block(self.inplanes, planes, groups=self.groups, base_width=self.base_width, dilation=self.dilation, norm_layer=norm_layer)
        self.block_6 = block(self.inplanes, planes, groups=self.groups, base_width=self.base_width, dilation=self.dilation, norm_layer=norm_layer)
