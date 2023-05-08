import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.nn.init as init
from torch.autograd import Variable
from core.config import cfg
import nn as mynn
import utils.net as net_utils


def __init__(self, dim_in):
    super().__init__()
    self.cls_score = nn.Linear(dim_in, cfg.MODEL.NUM_CLASSES)
    if cfg.MODEL.CLS_AGNOSTIC_BBOX_REG:
        self.bbox_pred = nn.Linear(dim_in, (4 * 2))
    else:
        self.bbox_pred = nn.Linear(dim_in, (4 * cfg.MODEL.NUM_CLASSES))
    self._init_weights()
