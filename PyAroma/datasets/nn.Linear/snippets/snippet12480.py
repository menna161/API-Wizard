import math
import torch.nn as nn
import torch.nn.functional as F
from FastAutoAugment.networks.shakeshake.shakeshake import ShakeShake
from FastAutoAugment.networks.shakeshake.shakeshake import Shortcut


def __init__(self, depth, w_base, label):
    super(ShakeResNet, self).__init__()
    n_units = ((depth - 2) / 6)
    in_chs = [16, w_base, (w_base * 2), (w_base * 4)]
    self.in_chs = in_chs
    self.c_in = nn.Conv2d(3, in_chs[0], 3, padding=1)
    self.layer1 = self._make_layer(n_units, in_chs[0], in_chs[1])
    self.layer2 = self._make_layer(n_units, in_chs[1], in_chs[2], 2)
    self.layer3 = self._make_layer(n_units, in_chs[2], in_chs[3], 2)
    self.fc_out = nn.Linear(in_chs[3], label)
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            n = ((m.kernel_size[0] * m.kernel_size[1]) * m.out_channels)
            m.weight.data.normal_(0, math.sqrt((2.0 / n)))
        elif isinstance(m, nn.BatchNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
        elif isinstance(m, nn.Linear):
            m.bias.data.zero_()
