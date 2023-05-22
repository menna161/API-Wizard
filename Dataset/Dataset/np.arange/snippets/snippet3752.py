import numpy as np
from numpy import linalg as la
import json
import logging
from torch import nn
from torch.nn import init
import torch.nn.functional as F
from core.config import cfg
from modeling_rel.generate_rel_proposal_labels import GenerateRelProposalLabelsOp
import modeling.FPN as FPN
import utils_rel.boxes_rel as box_utils_rel
import utils.fpn as fpn_utils
import numpy.random as npr
import utils.boxes as box_utils
import torch
from torch.autograd import Variable


def forward(self, det_rois, det_labels, det_scores, im_info, dataset_name, roidb=None):
    '\n        det_rois: feature maps from the backbone network. (Variable)\n        im_info: (CPU Variable)\n        roidb: (list of ndarray)\n        '
    if (roidb is not None):
        assert (len(roidb) == 1)
    sbj_inds = np.repeat(np.arange(det_rois.shape[0]), det_rois.shape[0])
    obj_inds = np.tile(np.arange(det_rois.shape[0]), det_rois.shape[0])
    if (det_rois.shape[0] > 1):
        (sbj_inds, obj_inds) = self.remove_self_pairs(det_rois.shape[0], sbj_inds, obj_inds)
    sbj_rois = det_rois[sbj_inds]
    obj_rois = det_rois[obj_inds]
    im_scale = im_info.data.numpy()[(:, 2)][0]
    sbj_boxes = (sbj_rois[(:, 1:)] / im_scale)
    obj_boxes = (obj_rois[(:, 1:)] / im_scale)
    if cfg.MODEL.USE_OVLP_FILTER:
        ovlp_so = box_utils_rel.bbox_pair_overlaps(sbj_boxes.astype(dtype=np.float32, copy=False), obj_boxes.astype(dtype=np.float32, copy=False))
        ovlp_inds = np.where((ovlp_so > 0))[0]
        sbj_inds = sbj_inds[ovlp_inds]
        obj_inds = obj_inds[ovlp_inds]
        sbj_rois = sbj_rois[ovlp_inds]
        obj_rois = obj_rois[ovlp_inds]
        sbj_boxes = sbj_boxes[ovlp_inds]
        obj_boxes = obj_boxes[ovlp_inds]
    return_dict = {}
    if self.training:
        blobs_out = self.RelPN_GenerateProposalLabels(sbj_rois, obj_rois, det_rois, roidb, im_info)
        return_dict.update(blobs_out)
    else:
        sbj_labels = det_labels[sbj_inds]
        obj_labels = det_labels[obj_inds]
        sbj_scores = det_scores[sbj_inds]
        obj_scores = det_scores[obj_inds]
        rel_rois = box_utils_rel.rois_union(sbj_rois, obj_rois)
        return_dict['det_rois'] = det_rois
        return_dict['sbj_inds'] = sbj_inds
        return_dict['obj_inds'] = obj_inds
        return_dict['sbj_rois'] = sbj_rois
        return_dict['obj_rois'] = obj_rois
        return_dict['rel_rois'] = rel_rois
        return_dict['sbj_labels'] = sbj_labels
        return_dict['obj_labels'] = obj_labels
        return_dict['sbj_scores'] = sbj_scores
        return_dict['obj_scores'] = obj_scores
        return_dict['fg_size'] = np.array([sbj_rois.shape[0]], dtype=np.int32)
        im_scale = im_info.data.numpy()[(:, 2)][0]
        im_w = im_info.data.numpy()[(:, 1)][0]
        im_h = im_info.data.numpy()[(:, 0)][0]
        if cfg.MODEL.USE_SPATIAL_FEAT:
            spt_feat = box_utils_rel.get_spt_features(sbj_boxes, obj_boxes, im_w, im_h)
            return_dict['spt_feat'] = spt_feat
        if (cfg.MODEL.USE_FREQ_BIAS or cfg.MODEL.RUN_BASELINE):
            return_dict['all_sbj_labels_int32'] = (sbj_labels.astype(np.int32, copy=False) - 1)
            return_dict['all_obj_labels_int32'] = (obj_labels.astype(np.int32, copy=False) - 1)
        if (cfg.FPN.FPN_ON and cfg.FPN.MULTILEVEL_ROIS):
            lvl_min = cfg.FPN.ROI_MIN_LEVEL
            lvl_max = cfg.FPN.ROI_MAX_LEVEL
            rois_blob_names = ['det_rois', 'rel_rois']
            for rois_blob_name in rois_blob_names:
                target_lvls = fpn_utils.map_rois_to_fpn_levels(return_dict[rois_blob_name][(:, 1:5)], lvl_min, lvl_max)
                fpn_utils.add_multilevel_roi_blobs(return_dict, rois_blob_name, return_dict[rois_blob_name], target_lvls, lvl_min, lvl_max)
    return return_dict
