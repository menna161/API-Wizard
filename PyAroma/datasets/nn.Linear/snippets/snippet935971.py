import logging
import torch
import torch.nn as nn
import torch.nn.functional as F
from mmcv.cnn import VGG, xavier_init, constant_init, kaiming_init, normal_init
from mmcv.runner import load_checkpoint
from ..registry import BACKBONES


def init_weights(self, pretrained=None):
    if isinstance(pretrained, str):
        logger = logging.getLogger()
        load_checkpoint(self, pretrained, strict=False, logger=logger)
    elif (pretrained is None):
        for m in self.features.modules():
            if isinstance(m, nn.Conv2d):
                kaiming_init(m)
            elif isinstance(m, nn.BatchNorm2d):
                constant_init(m, 1)
            elif isinstance(m, nn.Linear):
                normal_init(m, std=0.01)
    else:
        raise TypeError('pretrained must be a str or None')
    for m in self.extra.modules():
        if isinstance(m, nn.Conv2d):
            xavier_init(m, distribution='uniform')
    constant_init(self.l2_norm, self.l2_norm.scale)
