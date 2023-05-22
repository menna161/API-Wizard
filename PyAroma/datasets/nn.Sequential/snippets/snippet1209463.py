import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.utils.rnn import pack_padded_sequence, PackedSequence
import math
from lib.pytorch_convolutional_rnn import convolutional_rnn
import numpy as np


def _make_layer_scene(self, block, planes, blocks, stride=1):
    downsample = None
    if ((stride != 1) or (self.inplanes_scene != (planes * block.expansion))):
        downsample = nn.Sequential(nn.Conv2d(self.inplanes_scene, (planes * block.expansion), kernel_size=1, stride=stride, bias=False), nn.BatchNorm2d((planes * block.expansion)))
    layers = []
    layers.append(block(self.inplanes_scene, planes, stride, downsample))
    self.inplanes_scene = (planes * block.expansion)
    for i in range(1, blocks):
        layers.append(block(self.inplanes_scene, planes))
    return nn.Sequential(*layers)
