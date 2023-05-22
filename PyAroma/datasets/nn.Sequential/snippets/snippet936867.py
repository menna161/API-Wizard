import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
from functools import partial
from network.focal_loss import focal_loss
from network.utils import distance2bbox, iou_loss, giou_loss, volume, bbox_iou_loss
from post_processing.tube_nms import multiclass_nms


def _init_layers(self):
    self.cls_convs = nn.ModuleList()
    self.reg_convs = nn.ModuleList()
    for i in range(self.stacked_convs):
        chn = (self.in_channels if (i == 0) else self.feat_channels)
        self.cls_convs.append(nn.Sequential(nn.Conv3d(chn, self.feat_channels, kernel_size=3, stride=1, padding=1, bias=False), nn.GroupNorm(num_groups=32, num_channels=self.feat_channels), nn.ReLU(inplace=True)))
        self.reg_convs.append(nn.Sequential(nn.Conv3d(chn, self.feat_channels, kernel_size=3, stride=1, padding=1, bias=False), nn.GroupNorm(num_groups=32, num_channels=self.feat_channels), nn.ReLU(inplace=True)))
    self.TubeTK_cls = nn.Conv3d(self.feat_channels, self.cls_out_channels, 3, padding=1)
    self.TubeTK_reg = nn.Conv3d(self.feat_channels, self.tube_points, 3, padding=1)
    self.TubeTK_centerness = nn.Conv3d(self.feat_channels, 1, 3, padding=1)
    self.scales = nn.ModuleList([Scale(1.0) for _ in self.regress_ranges])
    for m in self.modules():
        if isinstance(m, nn.Conv3d):
            nn.init.normal_(m.weight, 0, 0.01)
            if (hasattr(m, 'bias') and (m.bias is not None)):
                nn.init.constant_(m.bias, 0)
        elif isinstance(m, nn.GroupNorm):
            m.weight.data.fill_(1)
            m.bias.data.zero_()
