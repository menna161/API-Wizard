import numpy as np
from numpy import linalg as la
import json
import logging
from torch import nn
from torch.nn import init
import torch
import torch.nn.functional as F
from torch.autograd import Variable
from core.config import cfg
from modeling_rel.generate_rel_proposal_labels import GenerateRelProposalLabelsOp
import modeling.FPN as FPN
import utils_rel.boxes_rel as box_utils_rel
import utils.fpn as fpn_utils
import numpy.random as npr
import utils.boxes as box_utils


def co_nms(self, p_det_rois, scores):
    pre_topN = (cfg.TRAIN.PRUNE_PAIRS_PRE_NMS_TOP_N if self.training else cfg.TEST.PRUNE_PAIRS_PRE_NMS_TOP_N)
    post_topN = (cfg.TRAIN.PRUNE_PAIRS_POST_NMS_TOP_N if self.training else cfg.TEST.PRUNE_PAIRS_POST_NMS_TOP_N)
    nms_thr = (cfg.TRAIN.PRUNE_PAIRS_NMS_THRESH if self.training else cfg.TEST.PRUNE_PAIRS_NMS_THRESH)
    if (p_det_rois.shape[0] > pre_topN):
        keep_inds = np.argsort((- scores.ravel()))[:pre_topN]
        p_det_rois = p_det_rois[keep_inds]
    else:
        keep_inds = np.arange(p_det_rois.shape[0], dtype=np.int64)
    p_dets = np.concatenate((p_det_rois, scores[keep_inds]), (- 1))
    keep_inds_nms = box_utils.co_nms(p_dets, nms_thr)
    keep_inds = keep_inds[keep_inds_nms]
    if (keep_inds.shape[0] > post_topN):
        sort_inds = np.argsort((- scores[keep_inds].ravel()))[:post_topN]
        keep_inds = keep_inds[sort_inds]
    return keep_inds
