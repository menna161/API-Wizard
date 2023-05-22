import math
import torch.nn as nn
import torch.nn.functional as F
from FastAutoAugment.networks.shakeshake.shakeshake import ShakeShake
from FastAutoAugment.networks.shakeshake.shakeshake import Shortcut


def _make_branch(self, in_ch, out_ch, stride=1):
    return nn.Sequential(nn.ReLU(inplace=False), nn.Conv2d(in_ch, out_ch, 3, padding=1, stride=stride, bias=False), nn.BatchNorm2d(out_ch), nn.ReLU(inplace=False), nn.Conv2d(out_ch, out_ch, 3, padding=1, stride=1, bias=False), nn.BatchNorm2d(out_ch))
