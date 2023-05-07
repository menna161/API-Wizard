from functools import wraps
import importlib
import logging
import numpy as np
import copy
import json
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from collections import defaultdict
from core.config import cfg
from model.roi_pooling.functions.roi_pool import RoIPoolFunction
from model.roi_crop.functions.roi_crop import RoICropFunction
from modeling.roi_xfrom.roi_align.functions.roi_align import RoIAlignFunction
import modeling.rpn_heads as rpn_heads
import modeling_rel.fast_rcnn_heads as fast_rcnn_heads
import modeling_rel.relpn_heads as relpn_heads
import modeling_rel.reldn_heads as reldn_heads
import modeling_rel.rel_pyramid_module as rel_pyramid_module
from modeling_rel.refine_obj_feats import Merge_OBJ_Feats, Message_Passing4OBJ
from modeling_rel.detector_builder import Generalized_RCNN
import utils_rel.boxes_rel as box_utils_rel
import utils.boxes as box_utils
import utils.blob as blob_utils
import utils_rel.net_rel as net_utils_rel
from utils.timer import Timer
import utils.resnet_weights_helper as resnet_utils
import utils.fpn as fpn_utils
from modeling_rel.sparse_targets_rel import FrequencyBias, FrequencyBias_Fix
from datasets_rel.pytorch_misc import intersect_2d
from math import pi


def get_rel_inds(self, det_rois, det_labels, roidb, im_info):
    num_img = (int(det_rois[(:, 0)].max()) + 1)
    im_inds = det_rois[(:, 0)].astype(np.int64)
    if self.training:
        return relpn_heads.rel_assignments(im_inds, det_rois, det_labels, roidb, im_info, num_sample_per_gt=1, filter_non_overlap=True)
    else:
        if cfg.TRAIN.GT_BOXES:
            fg_rels = []
            is_cand = (im_inds[(:, None)] == im_inds[None])
            is_cand[(np.arange(im_inds.shape[0]), np.arange(im_inds.shape[0]))] = False
            for i in range(num_img):
                gt_boxes_i = roidb[i]['boxes']
                sbj_gt_boxes_i = roidb[i]['sbj_gt_boxes']
                obj_gt_boxes_i = roidb[i]['obj_gt_boxes']
                sbj_gt_inds_i = box_utils.bbox_overlaps(sbj_gt_boxes_i, gt_boxes_i).argmax((- 1))
                obj_gt_inds_i = box_utils.bbox_overlaps(obj_gt_boxes_i, gt_boxes_i).argmax((- 1))
                im_id_i = (np.ones_like(sbj_gt_inds_i) * i)
                gt_rels_i = np.stack((im_id_i, sbj_gt_inds_i, obj_gt_inds_i), (- 1))
                fg_rels.append(gt_rels_i)
            rel_inds = np.concatenate(fg_rels, 0)
        else:
            is_cand = (im_inds[(:, None)] == im_inds[None])
            is_cand[(np.arange(im_inds.shape[0]), np.arange(im_inds.shape[0]))] = False
            is_cand = ((box_utils.bbox_overlaps(det_rois[(:, 1:)], det_rois[(:, 1:)]) > 0) & is_cand)
            (sbj_ind, obj_ind) = np.where(is_cand)
            if (len(sbj_ind) == 0):
                (sbj_ind, obj_ind) = (np.zeros(1, dtype=np.int64), np.zeros(1, dtype=np.int64))
            rel_inds = np.stack((det_rois[(sbj_ind, 0)].astype(sbj_ind.dtype), sbj_ind, obj_ind), (- 1))
        return (rel_inds, None)
