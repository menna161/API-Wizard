import math
import torch.nn as nn
import torch.nn.functional as F
from FastAutoAugment.networks.shakeshake.shakeshake import ShakeShake
from FastAutoAugment.networks.shakeshake.shakeshake import Shortcut


def _make_layer(self, n_units, n_ch, w_base, cardinary, stride=1):
    layers = []
    (mid_ch, out_ch) = (((n_ch * (w_base // 64)) * cardinary), (n_ch * 4))
    for i in range(n_units):
        layers.append(ShakeBottleNeck(self.in_ch, mid_ch, out_ch, cardinary, stride=stride))
        (self.in_ch, stride) = (out_ch, 1)
    return nn.Sequential(*layers)
