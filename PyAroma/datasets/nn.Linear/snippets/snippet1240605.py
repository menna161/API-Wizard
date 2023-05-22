import torch.nn as nn
from mmcv.cnn.weight_init import normal_init, xavier_init
from mmdet.ops import ConvModule
from ..backbones.resnet import Bottleneck
from ..registry import HEADS
from .bbox_head import BBoxHead


def __init__(self, num_convs=0, num_fcs=0, conv_out_channels=1024, fc_out_channels=1024, conv_cfg=None, norm_cfg=dict(type='BN'), **kwargs):
    kwargs.setdefault('with_avg_pool', True)
    super(DoubleConvFCBBoxHead, self).__init__(**kwargs)
    assert self.with_avg_pool
    assert (num_convs > 0)
    assert (num_fcs > 0)
    self.num_convs = num_convs
    self.num_fcs = num_fcs
    self.conv_out_channels = conv_out_channels
    self.fc_out_channels = fc_out_channels
    self.conv_cfg = conv_cfg
    self.norm_cfg = norm_cfg
    self.res_block = BasicResBlock(self.in_channels, self.conv_out_channels)
    self.conv_branch = self._add_conv_branch()
    self.fc_branch = self._add_fc_branch()
    out_dim_reg = (4 if self.reg_class_agnostic else (4 * self.num_classes))
    self.fc_reg = nn.Linear(self.conv_out_channels, out_dim_reg)
    self.fc_cls = nn.Linear(self.fc_out_channels, self.num_classes)
    self.relu = nn.ReLU(inplace=True)
