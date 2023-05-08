import numpy as np
from numpy import linalg as la
import math
import logging
import json
import torch
from torch import nn
from torch.nn import init
import torch.nn.functional as F
from torch.autograd import Variable
import nn as mynn
from core.config import cfg
from modeling_rel.sparse_targets_rel import FrequencyBias
from modeling_rel.draw_rectangles.draw_rectangles import draw_union_boxes


def __init__(self, dim_in):
    super().__init__()
    dim_in_final = (dim_in // 3)
    self.dim_in_final = dim_in_final
    if cfg.MODEL.USE_BG:
        num_prd_classes = (cfg.MODEL.NUM_PRD_CLASSES + 1)
    else:
        num_prd_classes = cfg.MODEL.NUM_PRD_CLASSES
    if cfg.MODEL.RUN_BASELINE:
        self.freq_bias = FrequencyBias(cfg.TEST.DATASETS[0])
        return
    self.prd_cls_feats = nn.Sequential(nn.Linear(dim_in, (dim_in // 2)), nn.LeakyReLU(0.1), nn.Linear((dim_in // 2), dim_in_final), nn.LeakyReLU(0.1))
    self.prd_cls_scores = nn.Linear(dim_in_final, num_prd_classes)
    if cfg.MODEL.USE_FREQ_BIAS:
        if len(cfg.TRAIN.DATASETS):
            self.freq_bias = FrequencyBias(cfg.TRAIN.DATASETS[0])
        else:
            self.freq_bias = FrequencyBias(cfg.TEST.DATASETS[0])
    if cfg.MODEL.USE_SPATIAL_FEAT:
        self.spt_cls_feats = nn.Sequential(nn.Linear(28, 64), nn.LeakyReLU(0.1), nn.Linear(64, 64), nn.LeakyReLU(0.1))
        self.spt_cls_scores = nn.Linear(64, num_prd_classes)
    if cfg.MODEL.ADD_SO_SCORES:
        self.prd_sbj_scores = nn.Linear(dim_in_final, num_prd_classes)
        self.prd_obj_scores = nn.Linear(dim_in_final, num_prd_classes)
    self._init_weights()
