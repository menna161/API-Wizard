import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.modules.utils import _pair
from mmdet.core import auto_fp16, bbox_target, delta2bbox, force_fp32, multiclass_nms
from ..builder import build_loss
from ..losses import accuracy
from ..registry import HEADS


def __init__(self, with_avg_pool=False, with_cls=True, with_reg=True, roi_feat_size=7, in_channels=256, num_classes=81, target_means=[0.0, 0.0, 0.0, 0.0], target_stds=[0.1, 0.1, 0.2, 0.2], reg_class_agnostic=False, loss_cls=dict(type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0), loss_bbox=dict(type='SmoothL1Loss', beta=1.0, loss_weight=1.0)):
    super(BBoxHead, self).__init__()
    assert (with_cls or with_reg)
    self.with_avg_pool = with_avg_pool
    self.with_cls = with_cls
    self.with_reg = with_reg
    self.roi_feat_size = _pair(roi_feat_size)
    self.roi_feat_area = (self.roi_feat_size[0] * self.roi_feat_size[1])
    self.in_channels = in_channels
    self.num_classes = num_classes
    self.target_means = target_means
    self.target_stds = target_stds
    self.reg_class_agnostic = reg_class_agnostic
    self.fp16_enabled = False
    self.loss_cls = build_loss(loss_cls)
    self.loss_bbox = build_loss(loss_bbox)
    in_channels = self.in_channels
    if self.with_avg_pool:
        self.avg_pool = nn.AvgPool2d(self.roi_feat_size)
    else:
        in_channels *= self.roi_feat_area
    if self.with_cls:
        self.fc_cls = nn.Linear(in_channels, num_classes)
    if self.with_reg:
        out_dim_reg = (4 if reg_class_agnostic else (4 * num_classes))
        self.fc_reg = nn.Linear(in_channels, out_dim_reg)
    self.debug_imgs = None
