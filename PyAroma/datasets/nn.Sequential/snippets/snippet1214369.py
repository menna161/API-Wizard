import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from modules.utils import *
from modules.losses import *
from libs.nms.nms_wrapper import nms


def __init__(self, in_channels, feature_stride, mode, cfg, **kwargs):
    super(RegionProposalNet, self).__init__()
    self.anchor_scales = cfg.ANCHOR_SCALES
    self.anchor_ratios = cfg.ANCHOR_RATIOS
    self.feature_stride = feature_stride
    self.mode = mode
    self.cfg = cfg
    self.rpn_conv_trans = nn.Sequential(nn.Conv2d(in_channels=in_channels, out_channels=512, kernel_size=3, stride=1, padding=1, bias=True), nn.ReLU(inplace=True))
    self.out_channels_cls = ((len(self.anchor_scales) * len(self.anchor_ratios)) * 2)
    self.out_channels_reg = ((len(self.anchor_scales) * len(self.anchor_ratios)) * 4)
    self.rpn_conv_cls = nn.Conv2d(in_channels=512, out_channels=self.out_channels_cls, kernel_size=1, stride=1, padding=0)
    self.rpn_conv_reg = nn.Conv2d(in_channels=512, out_channels=self.out_channels_reg, kernel_size=1, stride=1, padding=0)
    self.rpn_proposal_layer = rpnProposalLayer(feature_stride=self.feature_stride, anchor_scales=self.anchor_scales, anchor_ratios=self.anchor_ratios, mode=self.mode, cfg=self.cfg)
    self.rpn_build_target_layer = rpnBuildTargetLayer(feature_stride=self.feature_stride, anchor_scales=self.anchor_scales, anchor_ratios=self.anchor_ratios, mode=self.mode, cfg=self.cfg)
