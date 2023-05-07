import torch
import torch.nn as nn
from mmdet.core import bbox2result, bbox2roi, build_assigner, build_sampler
from .. import builder
from ..registry import DETECTORS
from .base import BaseDetector
from .test_mixins import BBoxTestMixin, MaskTestMixin, RPNTestMixin


def forward_dummy(self, img):
    'Used for computing network flops.\n\n        See `mmdetection/tools/get_flops.py`\n        '
    outs = ()
    x = self.extract_feat(img)
    if self.with_rpn:
        rpn_outs = self.rpn_head(x)
        outs = (outs + (rpn_outs,))
    proposals = torch.randn(1000, 4).to(device=img.device)
    rois = bbox2roi([proposals])
    if self.with_bbox:
        bbox_feats = self.bbox_roi_extractor(x[:self.bbox_roi_extractor.num_inputs], rois)
        if self.with_shared_head:
            bbox_feats = self.shared_head(bbox_feats)
        (cls_score, bbox_pred) = self.bbox_head(bbox_feats)
        outs = (outs + (cls_score, bbox_pred))
    if self.with_mask:
        mask_rois = rois[:100]
        mask_feats = self.mask_roi_extractor(x[:self.mask_roi_extractor.num_inputs], mask_rois)
        if self.with_shared_head:
            mask_feats = self.shared_head(mask_feats)
        mask_pred = self.mask_head(mask_feats)
        outs = (outs + (mask_pred,))
    return outs
