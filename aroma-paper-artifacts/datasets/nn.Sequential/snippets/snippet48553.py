from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import math
from os.path import join
import torch
from torch import nn
import torch.utils.model_zoo as model_zoo
import numpy as np


def __init__(self, base_name, heads, pretrained=True, down_ratio=4, head_conv=256):
    super(DLASeg, self).__init__()
    assert (down_ratio in [2, 4, 8, 16])
    self.heads = heads
    self.first_level = int(np.log2(down_ratio))
    self.base = globals()[base_name](pretrained=pretrained, return_levels=True)
    channels = self.base.channels
    scales = [(2 ** i) for i in range(len(channels[self.first_level:]))]
    self.dla_up = DLAUp(channels[self.first_level:], scales=scales)
    '\n        self.fc = nn.Sequential(\n            nn.Conv2d(channels[self.first_level], classes, kernel_size=1,\n                      stride=1, padding=0, bias=True)\n        )\n        '
    for head in self.heads:
        classes = self.heads[head]
        if (head_conv > 0):
            fc = nn.Sequential(nn.Conv2d(channels[self.first_level], head_conv, kernel_size=3, padding=1, bias=True), nn.ReLU(inplace=True), nn.Conv2d(head_conv, classes, kernel_size=1, stride=1, padding=0, bias=True))
            if ('hm' in head):
                fc[(- 1)].bias.data.fill_((- 2.19))
            else:
                fill_fc_weights(fc)
        else:
            fc = nn.Conv2d(channels[self.first_level], classes, kernel_size=1, stride=1, padding=0, bias=True)
            if ('hm' in head):
                fc.bias.data.fill_((- 2.19))
            else:
                fill_fc_weights(fc)
        self.__setattr__(head, fc)
    '\n        up_factor = 2 ** self.first_level\n        if up_factor > 1:\n            up = nn.ConvTranspose2d(classes, classes, up_factor * 2,\n                                    stride=up_factor, padding=up_factor // 2,\n                                    output_padding=0, groups=classes,\n                                    bias=False)\n            fill_up_weights(up)\n            up.weight.requires_grad = False\n        else:\n            up = Identity()\n        self.up = up\n        self.softmax = nn.LogSoftmax(dim=1)\n        \n\n        for m in self.fc.modules():\n            if isinstance(m, nn.Conv2d):\n                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels\n                m.weight.data.normal_(0, math.sqrt(2. / n))\n            elif isinstance(m, BatchNorm):\n                m.weight.data.fill_(1)\n                m.bias.data.zero_()\n        '
