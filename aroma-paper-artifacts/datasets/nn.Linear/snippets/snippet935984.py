import torch.nn as nn
from .bbox_head import BBoxHead
from ..registry import HEADS
from ..utils import ConvModule


def __init__(self, num_shared_convs=0, num_shared_fcs=0, num_cls_convs=0, num_cls_fcs=0, num_reg_convs=0, num_reg_fcs=0, conv_out_channels=256, fc_out_channels=1024, conv_cfg=None, norm_cfg=None, *args, **kwargs):
    super(ConvFCBBoxHead, self).__init__(*args, **kwargs)
    assert ((((((num_shared_convs + num_shared_fcs) + num_cls_convs) + num_cls_fcs) + num_reg_convs) + num_reg_fcs) > 0)
    if ((num_cls_convs > 0) or (num_reg_convs > 0)):
        assert (num_shared_fcs == 0)
    if (not self.with_cls):
        assert ((num_cls_convs == 0) and (num_cls_fcs == 0))
    if (not self.with_reg):
        assert ((num_reg_convs == 0) and (num_reg_fcs == 0))
    self.num_shared_convs = num_shared_convs
    self.num_shared_fcs = num_shared_fcs
    self.num_cls_convs = num_cls_convs
    self.num_cls_fcs = num_cls_fcs
    self.num_reg_convs = num_reg_convs
    self.num_reg_fcs = num_reg_fcs
    self.conv_out_channels = conv_out_channels
    self.fc_out_channels = fc_out_channels
    self.conv_cfg = conv_cfg
    self.norm_cfg = norm_cfg
    (self.shared_convs, self.shared_fcs, last_layer_dim) = self._add_conv_fc_branch(self.num_shared_convs, self.num_shared_fcs, self.in_channels, True)
    self.shared_out_channels = last_layer_dim
    (self.cls_convs, self.cls_fcs, self.cls_last_dim) = self._add_conv_fc_branch(self.num_cls_convs, self.num_cls_fcs, self.shared_out_channels)
    (self.reg_convs, self.reg_fcs, self.reg_last_dim) = self._add_conv_fc_branch(self.num_reg_convs, self.num_reg_fcs, self.shared_out_channels)
    if ((self.num_shared_fcs == 0) and (not self.with_avg_pool)):
        if (self.num_cls_fcs == 0):
            self.cls_last_dim *= (self.roi_feat_size * self.roi_feat_size)
        if (self.num_reg_fcs == 0):
            self.reg_last_dim *= (self.roi_feat_size * self.roi_feat_size)
    self.relu = nn.ReLU(inplace=True)
    if self.with_cls:
        self.fc_cls = nn.Linear(self.cls_last_dim, self.num_classes)
    if self.with_reg:
        out_dim_reg = (4 if self.reg_class_agnostic else (4 * self.num_classes))
        self.fc_reg = nn.Linear(self.reg_last_dim, out_dim_reg)
