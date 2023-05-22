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


def rel_assignments_gt_boxes(roidb, im_inds):
    fg_rels = []
    num_img = len(roidb)
    is_cand = (im_inds[(:, None)] == im_inds[None])
    is_cand[(np.arange(im_inds.shape[0]), np.arange(im_inds.shape[0]))] = False
    for i in range(num_img):
        gt_boxes_i = roidb[i]['boxes']
        sbj_gt_boxes_i = roidb[i]['sbj_gt_boxes']
        obj_gt_boxes_i = roidb[i]['obj_gt_boxes']
        prd_gt_classes_i = roidb[i]['prd_gt_classes']
        if cfg.MODEL.USE_BG:
            prd_gt_classes_i += 1
        sbj_gt_inds_i = box_utils.bbox_overlaps(sbj_gt_boxes_i, gt_boxes_i).argmax((- 1))
        obj_gt_inds_i = box_utils.bbox_overlaps(obj_gt_boxes_i, gt_boxes_i).argmax((- 1))
        im_id_i = (np.ones_like(sbj_gt_inds_i) * i)
        gt_rels_i = np.stack((im_id_i, sbj_gt_inds_i, obj_gt_inds_i, prd_gt_classes_i), (- 1))
        fg_rels.append(gt_rels_i)
    fg_rels = np.concatenate(fg_rels, 0)
    offset = {}
    for (i, s, e) in enumerate_by_image(im_inds):
        offset[i] = s
    for (i, s, e) in enumerate_by_image(fg_rels[(:, 0)]):
        fg_rels[(s:e, 1:3)] += offset[i]
    is_cand[(fg_rels[(:, 1)], fg_rels[(:, 2)])] = False
    num_fg = min(fg_rels.shape[0], int((cfg.TRAIN.FG_REL_SIZE_PER_IM * num_img)))
    if (fg_rels.shape[0] > num_fg):
        fg_ind = np.random.choice(fg_rels.shape[0], num_fg, replace=False)
        fg_rels = fg_rels[fg_ind]
    (sbj_bg_inds, obj_bg_inds) = np.where(is_cand)
    bg_rels = np.stack((im_inds[sbj_bg_inds].astype(sbj_bg_inds.dtype), sbj_bg_inds, obj_bg_inds, np.zeros_like(sbj_bg_inds)), (- 1))
    num_bg = min(bg_rels.shape[0], int((((cfg.TRAIN.FG_REL_SIZE_PER_IM / cfg.TRAIN.FG_REL_FRACTION) * num_img) - num_fg)))
    if (num_bg > 0):
        if (bg_rels.shape[0] > num_bg):
            bg_ind = np.random.choice(bg_rels.shape[0], num_bg, replace=False)
            bg_rels = bg_rels[bg_ind]
        rel_labels = np.concatenate((fg_rels, bg_rels), 0)
    else:
        rel_labels = fg_rels
    return (rel_labels[(:, :(- 1))], rel_labels)
