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


def __init__(self):
    super().__init__()
    self.detector = Generalized_RCNN()
    self.obj_dim = self.detector.Box_Head.dim_out
    self.Box_Head_sg = get_func(cfg.FAST_RCNN.ROI_BOX_HEAD)(self.detector.RPN.dim_out, self.roi_feature_transform, self.detector.Conv_Body.spatial_scale)
    self.Box_Head_prd = get_func(cfg.FAST_RCNN.ROI_BOX_HEAD_PRD)(self.detector.RPN.dim_out, self.roi_feature_transform, self.detector.Conv_Body.spatial_scale)
    self.union_mask = reldn_heads.union_mask(self.detector.RPN.dim_out)
    self.ori_embed = get_ort_embeds(cfg.MODEL.NUM_CLASSES, 200)
    self.merge_obj_feats = Merge_OBJ_Feats(self.obj_dim, 200, 512)
    self.obj_mps1 = Message_Passing4OBJ(512)
    self.obj_mps2 = Message_Passing4OBJ(512)
    self.ObjClassifier = nn.Linear(512, cfg.MODEL.NUM_CLASSES)
    if cfg.MODEL.USE_FREQ_BIAS:
        if len(cfg.TRAIN.DATASETS):
            self.freq_bias = FrequencyBias_Fix(cfg.TRAIN.DATASETS[0])
        else:
            self.freq_bias = FrequencyBias_Fix(cfg.TEST.DATASETS[0])
    if cfg.MODEL.USE_BG:
        self.num_prd_classes = (cfg.MODEL.NUM_PRD_CLASSES + 1)
    else:
        self.num_prd_classes = cfg.MODEL.NUM_PRD_CLASSES
    self.get_phr_feats = nn.Linear(self.obj_dim, 512)
    self.merge_high = nn.Linear(512, self.obj_dim)
    self.merge_high.weight = torch.nn.init.xavier_normal_(self.merge_high.weight, gain=1.0)
    self.merge_low = nn.Linear(((self.obj_dim + 200) + 5), self.obj_dim)
    self.merge_low.weight = torch.nn.init.xavier_normal_(self.merge_low.weight, gain=1.0)
    self.sbj_map = nn.Linear(self.obj_dim, self.obj_dim)
    self.sbj_map.weight = torch.nn.init.xavier_normal_(self.sbj_map.weight, gain=1.0)
    self.obj_map = nn.Linear(self.obj_dim, self.obj_dim)
    self.obj_map.weight = torch.nn.init.xavier_normal_(self.obj_map.weight, gain=1.0)
    self.rel_compress = nn.Linear(self.obj_dim, self.num_prd_classes)
    self.rel_compress.weight = torch.nn.init.xavier_normal_(self.rel_compress.weight, gain=1.0)
    self.__init_modules()
