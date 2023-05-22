import os
import sys
from public.path import pretrained_models_path
import torch
import torch.nn as nn
import torch.nn.functional as F


def _make_layer(self, block, inplanes, planes, blocks, stride=1):
    downsample = None
    if ((stride != 1) or (inplanes != (planes * block.expansion))):
        downsample = nn.Sequential(nn.Conv2d(inplanes, (planes * block.expansion), kernel_size=1, stride=stride, bias=False), nn.BatchNorm2d((planes * block.expansion)))
    layers = []
    layers.append(block(inplanes, planes, stride, downsample))
    inplanes = (planes * block.expansion)
    for i in range(1, blocks):
        layers.append(block(inplanes, planes))
    return nn.Sequential(*layers)
