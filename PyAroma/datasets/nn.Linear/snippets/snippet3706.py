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


def _init_weights(self):
    for m in self.modules():
        if (isinstance(m, nn.Conv2d) or isinstance(m, nn.Linear)):
            mynn.init.XavierFill(m.weight)
            if (m.bias is not None):
                nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.BatchNorm2d):
            nn.init.constant_(m.weight, 1)
            nn.init.constant_(m.bias, 0)
