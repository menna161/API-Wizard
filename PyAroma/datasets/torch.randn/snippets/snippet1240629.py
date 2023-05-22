from __future__ import division
import torch
import torch.nn as nn
from mmdet.core import bbox2result, bbox2roi, bbox_mapping, build_assigner, build_sampler, merge_aug_bboxes, merge_aug_masks, multiclass_nms
from .. import builder
from ..registry import DETECTORS
from .base import BaseDetector
from .test_mixins import RPNTestMixin


def forward_dummy(self, img):
    outs = ()
    x = self.extract_feat(img)
    if self.with_rpn:
        rpn_outs = self.rpn_head(x)
        outs = (outs + (rpn_outs,))
    proposals = torch.randn(1000, 4).to(device=img.device)
    rois = bbox2roi([proposals])
    if self.with_bbox:
        for i in range(self.num_stages):
            bbox_feats = self.bbox_roi_extractor[i](x[:self.bbox_roi_extractor[i].num_inputs], rois)
            if self.with_shared_head:
                bbox_feats = self.shared_head(bbox_feats)
            (cls_score, bbox_pred) = self.bbox_head[i](bbox_feats)
            outs = (outs + (cls_score, bbox_pred))
    if self.with_mask:
        mask_rois = rois[:100]
        for i in range(self.num_stages):
            mask_feats = self.mask_roi_extractor[i](x[:self.mask_roi_extractor[i].num_inputs], mask_rois)
            if self.with_shared_head:
                mask_feats = self.shared_head(mask_feats)
            mask_pred = self.mask_head[i](mask_feats)
            outs = (outs + (mask_pred,))
    return outs
