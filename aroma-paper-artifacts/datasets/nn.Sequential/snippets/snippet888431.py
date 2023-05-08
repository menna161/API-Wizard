import numpy as np
import math
import torch
import torch.nn as nn
import torch.nn.functional as F


def _make_layer(self, block, in_planes, out_planes, nb_layers, stride, dropRate):
    layers = []
    for i in range(nb_layers):
        layers.append(block((((i == 0) and in_planes) or out_planes), out_planes, (((i == 0) and stride) or 1), dropRate))
    return nn.Sequential(*layers)
