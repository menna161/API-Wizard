import numpy as np
import torch
import torch.nn as nn
from mmcv.cnn import kaiming_init, normal_init
from ..builder import build_loss
from ..registry import HEADS


def __init__(self, num_convs=4, num_fcs=2, roi_feat_size=14, in_channels=256, conv_out_channels=256, fc_out_channels=1024, num_classes=81, loss_iou=dict(type='MSELoss', loss_weight=0.5)):
    super(MaskIoUHead, self).__init__()
    self.in_channels = in_channels
    self.conv_out_channels = conv_out_channels
    self.fc_out_channels = fc_out_channels
    self.num_classes = num_classes
    self.convs = nn.ModuleList()
    for i in range(num_convs):
        if (i == 0):
            in_channels = (self.in_channels + 1)
        else:
            in_channels = self.conv_out_channels
        stride = (2 if (i == (num_convs - 1)) else 1)
        self.convs.append(nn.Conv2d(in_channels, self.conv_out_channels, 3, stride=stride, padding=1))
    self.fcs = nn.ModuleList()
    for i in range(num_fcs):
        in_channels = ((self.conv_out_channels * ((roi_feat_size // 2) ** 2)) if (i == 0) else self.fc_out_channels)
        self.fcs.append(nn.Linear(in_channels, self.fc_out_channels))
    self.fc_mask_iou = nn.Linear(self.fc_out_channels, self.num_classes)
    self.relu = nn.ReLU()
    self.max_pool = nn.MaxPool2d(2, 2)
    self.loss_iou = build_loss(loss_iou)
