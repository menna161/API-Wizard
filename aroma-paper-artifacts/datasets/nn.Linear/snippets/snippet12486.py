import math
import torch.nn as nn
import torch.nn.functional as F
from FastAutoAugment.networks.shakeshake.shakeshake import ShakeShake
from FastAutoAugment.networks.shakeshake.shakeshake import Shortcut


def __init__(self, depth, w_base, cardinary, label):
    super(ShakeResNeXt, self).__init__()
    n_units = ((depth - 2) // 9)
    n_chs = [64, 128, 256, 1024]
    self.n_chs = n_chs
    self.in_ch = n_chs[0]
    self.c_in = nn.Conv2d(3, n_chs[0], 3, padding=1)
    self.layer1 = self._make_layer(n_units, n_chs[0], w_base, cardinary)
    self.layer2 = self._make_layer(n_units, n_chs[1], w_base, cardinary, 2)
    self.layer3 = self._make_layer(n_units, n_chs[2], w_base, cardinary, 2)
    self.fc_out = nn.Linear(n_chs[3], label)
    for m in self.modules():
        if isinstance(m, nn.Conv2d):
            n = ((m.kernel_size[0] * m.kernel_size[1]) * m.out_channels)
            m.weight.data.normal_(0, math.sqrt((2.0 / n)))
        elif isinstance(m, nn.BatchNorm2d):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
        elif isinstance(m, nn.Linear):
            m.bias.data.zero_()
