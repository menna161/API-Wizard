import torch
import torch.nn as nn
import torch.nn.functional as F


def _make_stage(self, repeat, in_channels, out_channels, stride, t):
    layers = []
    layers.append(LinearBottleNeck(in_channels, out_channels, stride, t))
    while (repeat - 1):
        layers.append(LinearBottleNeck(out_channels, out_channels, 1, t))
        repeat -= 1
    return nn.Sequential(*layers)
