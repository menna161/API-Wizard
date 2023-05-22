from typing import List, Optional, Tuple
import torch
import torch.nn as nn
import torch.nn.functional as F
from pointnet2_ops import pointnet2_utils


def build_shared_mlp(mlp_spec: List[int], bn: bool=True):
    layers = []
    for i in range(1, len(mlp_spec)):
        layers.append(nn.Conv2d(mlp_spec[(i - 1)], mlp_spec[i], kernel_size=1, bias=(not bn)))
        if bn:
            layers.append(nn.BatchNorm2d(mlp_spec[i]))
        layers.append(nn.ReLU(True))
    return nn.Sequential(*layers)
