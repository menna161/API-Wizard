import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from mmcv.cnn import kaiming_init, normal_init
from ..builder import build_loss
from ..registry import HEADS
from ..utils import ConvModule


def __init__(self, grid_points=9, num_convs=8, roi_feat_size=14, in_channels=256, conv_kernel_size=3, point_feat_channels=64, deconv_kernel_size=4, class_agnostic=False, loss_grid=dict(type='CrossEntropyLoss', use_sigmoid=True, loss_weight=15), conv_cfg=None, norm_cfg=dict(type='GN', num_groups=36)):
    super(GridHead, self).__init__()
    self.grid_points = grid_points
    self.num_convs = num_convs
    self.roi_feat_size = roi_feat_size
    self.in_channels = in_channels
    self.conv_kernel_size = conv_kernel_size
    self.point_feat_channels = point_feat_channels
    self.conv_out_channels = (self.point_feat_channels * self.grid_points)
    self.class_agnostic = class_agnostic
    self.conv_cfg = conv_cfg
    self.norm_cfg = norm_cfg
    if (isinstance(norm_cfg, dict) and (norm_cfg['type'] == 'GN')):
        assert ((self.conv_out_channels % norm_cfg['num_groups']) == 0)
    assert (self.grid_points >= 4)
    self.grid_size = int(np.sqrt(self.grid_points))
    if ((self.grid_size * self.grid_size) != self.grid_points):
        raise ValueError('grid_points must be a square number')
    self.whole_map_size = (self.roi_feat_size * 4)
    self.sub_regions = self.calc_sub_regions()
    self.convs = []
    for i in range(self.num_convs):
        in_channels = (self.in_channels if (i == 0) else self.conv_out_channels)
        stride = (2 if (i == 0) else 1)
        padding = ((self.conv_kernel_size - 1) // 2)
        self.convs.append(ConvModule(in_channels, self.conv_out_channels, self.conv_kernel_size, stride=stride, padding=padding, conv_cfg=self.conv_cfg, norm_cfg=self.norm_cfg, bias=True))
    self.convs = nn.Sequential(*self.convs)
    self.deconv1 = nn.ConvTranspose2d(self.conv_out_channels, self.conv_out_channels, kernel_size=deconv_kernel_size, stride=2, padding=((deconv_kernel_size - 2) // 2), groups=grid_points)
    self.norm1 = nn.GroupNorm(grid_points, self.conv_out_channels)
    self.deconv2 = nn.ConvTranspose2d(self.conv_out_channels, grid_points, kernel_size=deconv_kernel_size, stride=2, padding=((deconv_kernel_size - 2) // 2), groups=grid_points)
    self.neighbor_points = []
    grid_size = self.grid_size
    for i in range(grid_size):
        for j in range(grid_size):
            neighbors = []
            if (i > 0):
                neighbors.append((((i - 1) * grid_size) + j))
            if (j > 0):
                neighbors.append((((i * grid_size) + j) - 1))
            if (j < (grid_size - 1)):
                neighbors.append((((i * grid_size) + j) + 1))
            if (i < (grid_size - 1)):
                neighbors.append((((i + 1) * grid_size) + j))
            self.neighbor_points.append(tuple(neighbors))
    self.num_edges = sum([len(p) for p in self.neighbor_points])
    self.forder_trans = nn.ModuleList()
    self.sorder_trans = nn.ModuleList()
    for neighbors in self.neighbor_points:
        fo_trans = nn.ModuleList()
        so_trans = nn.ModuleList()
        for _ in range(len(neighbors)):
            fo_trans.append(nn.Sequential(nn.Conv2d(self.point_feat_channels, self.point_feat_channels, 5, stride=1, padding=2, groups=self.point_feat_channels), nn.Conv2d(self.point_feat_channels, self.point_feat_channels, 1)))
            so_trans.append(nn.Sequential(nn.Conv2d(self.point_feat_channels, self.point_feat_channels, 5, 1, 2, groups=self.point_feat_channels), nn.Conv2d(self.point_feat_channels, self.point_feat_channels, 1)))
        self.forder_trans.append(fo_trans)
        self.sorder_trans.append(so_trans)
    self.loss_grid = build_loss(loss_grid)
