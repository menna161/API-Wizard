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


def union_pairs(self, im_inds):
    rel_cands = (im_inds[(:, None)] == im_inds[None])
    rel_cands[(np.arange(im_inds.shape[0]), np.arange(im_inds.shape[0]))] = False
    empty_ind = np.where(np.logical_not(rel_cands.any((- 1))))[0]
    if (empty_ind.size > 0):
        rel_cands[(empty_ind, empty_ind)] = True
    (sbj_ind, obj_ind) = np.where(rel_cands)
    return np.stack((im_inds[sbj_ind].astype(sbj_ind.dtype), sbj_ind, obj_ind), (- 1))
