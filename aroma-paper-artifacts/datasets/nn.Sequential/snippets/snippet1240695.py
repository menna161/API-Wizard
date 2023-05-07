import torch
import torch.nn as nn
from mmdet.core import bbox2result, bbox2roi, build_assigner, build_sampler
from .. import builder
from ..registry import DETECTORS
from .base import BaseDetector
from .test_mixins import BBoxTestMixin, MaskTestMixin, RPNTestMixin


def init_weights(self, pretrained=None):
    super(TwoStageDetector, self).init_weights(pretrained)
    self.backbone.init_weights(pretrained=pretrained)
    if self.with_neck:
        if isinstance(self.neck, nn.Sequential):
            for m in self.neck:
                m.init_weights()
        else:
            self.neck.init_weights()
    if self.with_shared_head:
        self.shared_head.init_weights(pretrained=pretrained)
    if self.with_rpn:
        self.rpn_head.init_weights()
    if self.with_bbox:
        self.bbox_roi_extractor.init_weights()
        self.bbox_head.init_weights()
    if self.with_mask:
        self.mask_head.init_weights()
        if (not self.share_roi_extractor):
            self.mask_roi_extractor.init_weights()
