from .two_stage import TwoStageDetector
from ..registry import DETECTORS
import torch
from .. import builder
from mmdet.core import bbox2roi, bbox2result, build_assigner, build_sampler


def forward_train(self, img, img_meta, gt_bboxes, gt_labels, gt_bboxes_ignore=None, gt_masks=None, proposals=None):
    x = self.extract_feat(img)
    losses = dict()
    if self.with_rpn:
        rpn_outs = self.rpn_head(x)
        rpn_loss_inputs = (rpn_outs + (gt_bboxes, img_meta, self.train_cfg.rpn))
        rpn_losses = self.rpn_head.loss(*rpn_loss_inputs, gt_bboxes_ignore=gt_bboxes_ignore)
        losses.update(rpn_losses)
        proposal_cfg = self.train_cfg.get('rpn_proposal', self.test_cfg.rpn)
        proposal_inputs = (rpn_outs + (img_meta, proposal_cfg))
        proposal_list = self.rpn_head.get_bboxes(*proposal_inputs)
    else:
        proposal_list = proposals
    if self.with_bbox:
        bbox_assigner = build_assigner(self.train_cfg.rcnn.assigner)
        bbox_sampler = build_sampler(self.train_cfg.rcnn.sampler, context=self)
        num_imgs = img.size(0)
        if (gt_bboxes_ignore is None):
            gt_bboxes_ignore = [None for _ in range(num_imgs)]
        sampling_results = []
        for i in range(num_imgs):
            assign_result = bbox_assigner.assign(proposal_list[i], gt_bboxes[i], gt_bboxes_ignore[i], gt_labels[i])
            sampling_result = bbox_sampler.sample(assign_result, proposal_list[i], gt_bboxes[i], gt_labels[i], feats=[lvl_feat[i][None] for lvl_feat in x])
            sampling_results.append(sampling_result)
        rois = bbox2roi([res.bboxes for res in sampling_results])
        bbox_feats = self.bbox_roi_extractor(x[:self.bbox_roi_extractor.num_inputs], rois)
        if self.with_shared_head:
            bbox_feats = self.shared_head(bbox_feats)
        (cls_score, bbox_pred) = self.bbox_head(bbox_feats)
        bbox_targets = self.bbox_head.get_target(sampling_results, gt_bboxes, gt_labels, self.train_cfg.rcnn)
        loss_bbox = self.bbox_head.loss(cls_score, bbox_pred, *bbox_targets)
        losses.update(loss_bbox)
        sampling_results = self._random_jitter(sampling_results, img_meta)
        pos_rois = bbox2roi([res.pos_bboxes for res in sampling_results])
        grid_feats = self.grid_roi_extractor(x[:self.grid_roi_extractor.num_inputs], pos_rois)
        if self.with_shared_head:
            grid_feats = self.shared_head(grid_feats)
        max_sample_num_grid = self.train_cfg.rcnn.get('max_num_grid', 192)
        sample_idx = torch.randperm(grid_feats.shape[0])[:min(grid_feats.shape[0], max_sample_num_grid)]
        grid_feats = grid_feats[sample_idx]
        grid_pred = self.grid_head(grid_feats)
        grid_targets = self.grid_head.get_target(sampling_results, self.train_cfg.rcnn)
        grid_targets = grid_targets[sample_idx]
        loss_grid = self.grid_head.loss(grid_pred, grid_targets)
        losses.update(loss_grid)
    return losses
