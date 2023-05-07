import torch
from mmdet.core import bbox2roi, build_assigner, build_sampler
from ..registry import DETECTORS
from .two_stage import TwoStageDetector


def forward_dummy(self, img):
    outs = ()
    x = self.extract_feat(img)
    if self.with_rpn:
        rpn_outs = self.rpn_head(x)
        outs = (outs + (rpn_outs,))
    proposals = torch.randn(1000, 4).to(device=img.device)
    rois = bbox2roi([proposals])
    bbox_cls_feats = self.bbox_roi_extractor(x[:self.bbox_roi_extractor.num_inputs], rois)
    bbox_reg_feats = self.bbox_roi_extractor(x[:self.bbox_roi_extractor.num_inputs], rois, roi_scale_factor=self.reg_roi_scale_factor)
    if self.with_shared_head:
        bbox_cls_feats = self.shared_head(bbox_cls_feats)
        bbox_reg_feats = self.shared_head(bbox_reg_feats)
    (cls_score, bbox_pred) = self.bbox_head(bbox_cls_feats, bbox_reg_feats)
    outs += (cls_score, bbox_pred)
    return outs
