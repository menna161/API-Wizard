import torch.nn as nn
from mmdet.core import bbox2result
from .. import builder
from ..registry import DETECTORS
from .base import BaseDetector


def init_weights(self, pretrained=None):
    super(SingleStageDetector, self).init_weights(pretrained)
    self.backbone.init_weights(pretrained=pretrained)
    if self.with_neck:
        if isinstance(self.neck, nn.Sequential):
            for m in self.neck:
                m.init_weights()
        else:
            self.neck.init_weights()
    self.bbox_head.init_weights()