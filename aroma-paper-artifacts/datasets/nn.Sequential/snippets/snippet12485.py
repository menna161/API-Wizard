import math
import torch.nn as nn
import torch.nn.functional as F
from FastAutoAugment.networks.shakeshake.shakeshake import ShakeShake
from FastAutoAugment.networks.shakeshake.shakeshake import Shortcut


def _make_branch(self, in_ch, mid_ch, out_ch, cardinary, stride=1):
    return nn.Sequential(nn.Conv2d(in_ch, mid_ch, 1, padding=0, bias=False), nn.BatchNorm2d(mid_ch), nn.ReLU(inplace=False), nn.Conv2d(mid_ch, mid_ch, 3, padding=1, stride=stride, groups=cardinary, bias=False), nn.BatchNorm2d(mid_ch), nn.ReLU(inplace=False), nn.Conv2d(mid_ch, out_ch, 1, padding=0, bias=False), nn.BatchNorm2d(out_ch))
