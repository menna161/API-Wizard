import math
import torch.nn as nn
import torch.nn.functional as F
from FastAutoAugment.networks.shakeshake.shakeshake import ShakeShake
from FastAutoAugment.networks.shakeshake.shakeshake import Shortcut


def _make_layer(self, n_units, in_ch, out_ch, stride=1):
    layers = []
    for i in range(int(n_units)):
        layers.append(ShakeBlock(in_ch, out_ch, stride=stride))
        (in_ch, stride) = (out_ch, 1)
    return nn.Sequential(*layers)
