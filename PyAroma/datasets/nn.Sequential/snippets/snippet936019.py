from __future__ import division
import torch
import torch.nn as nn
from .base import BaseDetector
from .test_mixins import RPNTestMixin
from .. import builder
from ..registry import DETECTORS
from mmdet.core import build_assigner, bbox2roi, bbox2result, build_sampler, merge_aug_masks


def init_weights(self, pretrained=None):
    super(CascadeRCNN, self).init_weights(pretrained)
    self.backbone.init_weights(pretrained=pretrained)
    if self.with_neck:
        if isinstance(self.neck, nn.Sequential):
            for m in self.neck:
                m.init_weights()
        else:
            self.neck.init_weights()
    if self.with_rpn:
        self.rpn_head.init_weights()
    if self.with_shared_head:
        self.shared_head.init_weights(pretrained=pretrained)
    for i in range(self.num_stages):
        if self.with_bbox:
            self.bbox_roi_extractor[i].init_weights()
            self.bbox_head[i].init_weights()
        if self.with_mask:
            if (not self.share_roi_extractor):
                self.mask_roi_extractor[i].init_weights()
            self.mask_head[i].init_weights()
