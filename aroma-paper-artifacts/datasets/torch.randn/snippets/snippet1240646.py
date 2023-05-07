import torch
from mmdet.core import bbox2result, bbox2roi, build_assigner, build_sampler
from .. import builder
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
    bbox_feats = self.bbox_roi_extractor(x[:self.bbox_roi_extractor.num_inputs], rois)
    if self.with_shared_head:
        bbox_feats = self.shared_head(bbox_feats)
    (cls_score, bbox_pred) = self.bbox_head(bbox_feats)
    grid_rois = rois[:100]
    grid_feats = self.grid_roi_extractor(x[:self.grid_roi_extractor.num_inputs], grid_rois)
    if self.with_shared_head:
        grid_feats = self.shared_head(grid_feats)
    grid_pred = self.grid_head(grid_feats)
    return (rpn_outs, cls_score, bbox_pred, grid_pred)
