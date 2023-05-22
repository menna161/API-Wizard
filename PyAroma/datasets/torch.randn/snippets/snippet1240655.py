import torch
import torch.nn.functional as F
from mmdet.core import bbox2result, bbox2roi, bbox_mapping, build_assigner, build_sampler, merge_aug_bboxes, merge_aug_masks, multiclass_nms
from .. import builder
from ..registry import DETECTORS
from .cascade_rcnn import CascadeRCNN


def forward_dummy(self, img):
    outs = ()
    x = self.extract_feat(img)
    if self.with_rpn:
        rpn_outs = self.rpn_head(x)
        outs = (outs + (rpn_outs,))
    proposals = torch.randn(1000, 4).to(device=img.device)
    if self.with_semantic:
        (_, semantic_feat) = self.semantic_head(x)
    else:
        semantic_feat = None
    rois = bbox2roi([proposals])
    for i in range(self.num_stages):
        (cls_score, bbox_pred) = self._bbox_forward_test(i, x, rois, semantic_feat=semantic_feat)
        outs = (outs + (cls_score, bbox_pred))
    if self.with_mask:
        mask_rois = rois[:100]
        mask_roi_extractor = self.mask_roi_extractor[(- 1)]
        mask_feats = mask_roi_extractor(x[:len(mask_roi_extractor.featmap_strides)], mask_rois)
        if (self.with_semantic and ('mask' in self.semantic_fusion)):
            mask_semantic_feat = self.semantic_roi_extractor([semantic_feat], mask_rois)
            mask_feats += mask_semantic_feat
        last_feat = None
        for i in range(self.num_stages):
            mask_head = self.mask_head[i]
            if self.mask_info_flow:
                (mask_pred, last_feat) = mask_head(mask_feats, last_feat)
            else:
                mask_pred = mask_head(mask_feats)
            outs = (outs + (mask_pred,))
    return outs
