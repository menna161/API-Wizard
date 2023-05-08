import torch
import torch.nn as nn
import math
import torch.utils.model_zoo as model_zoo
import torch.distributed as dist


def _make_layer(self, block, planes, blocks, stride=1, avg_down=False):
    downsample = None
    if ((stride != 1) or (self.inplanes != (planes * block.expansion))):
        if self.avg_down:
            downsample = nn.Sequential(nn.AvgPool2d(stride, stride=stride, ceil_mode=True, count_include_pad=False), nn.Conv2d(self.inplanes, (planes * block.expansion), kernel_size=1, stride=1, bias=False), nn.BatchNorm2d((planes * block.expansion)))
        else:
            downsample = nn.Sequential(nn.Conv2d(self.inplanes, (planes * block.expansion), kernel_size=1, stride=stride, bias=False), nn.BatchNorm2d((planes * block.expansion)))
    layers = []
    layers.append(block(self.inplanes, planes, stride, downsample))
    self.inplanes = (planes * block.expansion)
    for i in range(1, blocks):
        layers.append(block(self.inplanes, planes))
    return nn.Sequential(*layers)
