import torch
import torch.nn as nn
from lib.sa.modules import Subtraction, Subtraction2, Aggregation


def _make_layer(self, sa_type, block, planes, blocks, kernel_size=7, stride=1):
    layers = []
    for _ in range(0, blocks):
        layers.append(block(sa_type, planes, (planes // 16), (planes // 4), planes, 8, kernel_size, stride))
    return nn.Sequential(*layers)
