import math
import torch
import torch.nn as nn


def _make_layer(self, planes, blocks, dropout, stride=1):
    layers = []
    for i in range(blocks):
        layers.append(BasicBlock(self.inplanes, planes, dropout, (stride if (i == 0) else 1)))
        self.inplanes = planes
    return nn.Sequential(*layers)
