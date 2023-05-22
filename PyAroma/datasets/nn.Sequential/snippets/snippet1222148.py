import time
import os
import torch
import torch.nn as nn
import torch.nn.functional as F


def _make_btlayer(self, bt, inChannels, outChannels, numBlock, t=6, stride=1):
    layers = []
    layers.append(bt(inChannels, outChannels, t, stride))
    for i in range(1, numBlock):
        layers.append(bt(outChannels, outChannels, t, 1))
    return nn.Sequential(*layers)
