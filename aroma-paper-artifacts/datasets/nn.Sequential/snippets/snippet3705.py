import collections
import numpy as np
import logging
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import init
from core.config import cfg
import utils.net as net_utils
import modeling.ResNet as ResNet
from modeling.generate_anchors import generate_anchors
from modeling.generate_proposals import GenerateProposalsOp
from modeling.collect_and_distribute_fpn_rpn_proposals import CollectAndDistributeFpnRpnProposalsOp
import nn as mynn


def __init__(self, num_backbone_stages):
    super().__init__()
    fpn_dim = cfg.FPN.DIM
    self.num_backbone_stages = num_backbone_stages
    self.prd_conv_lateral = nn.ModuleList()
    for i in range(self.num_backbone_stages):
        if cfg.FPN.USE_GN:
            self.prd_conv_lateral.append(nn.Sequential(nn.Conv2d(fpn_dim, fpn_dim, 1, 1, 0, bias=False), nn.GroupNorm(net_utils.get_group_gn(fpn_dim), fpn_dim, eps=cfg.GROUP_NORM.EPSILON)))
        else:
            self.prd_conv_lateral.append(nn.Conv2d(fpn_dim, fpn_dim, 1, 1, 0))
    self.posthoc_modules = nn.ModuleList()
    for i in range(self.num_backbone_stages):
        if cfg.FPN.USE_GN:
            self.posthoc_modules.append(nn.Sequential(nn.Conv2d(fpn_dim, fpn_dim, 3, 1, 1, bias=False), nn.GroupNorm(net_utils.get_group_gn(fpn_dim), fpn_dim, eps=cfg.GROUP_NORM.EPSILON)))
        else:
            self.posthoc_modules.append(nn.Conv2d(fpn_dim, fpn_dim, 3, 1, 1))
    self._init_weights()
