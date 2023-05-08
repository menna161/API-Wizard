import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from mmcv.cnn import kaiming_init, normal_init
from ..builder import build_loss
from ..registry import HEADS
from ..utils import ConvModule


def init_weights(self):
    for m in self.modules():
        if (isinstance(m, nn.Conv2d) or isinstance(m, nn.Linear)):
            kaiming_init(m)
    for m in self.modules():
        if isinstance(m, nn.ConvTranspose2d):
            normal_init(m, std=0.001)
    nn.init.constant_(self.deconv2.bias, (- np.log((0.99 / 0.01))))
