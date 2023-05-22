from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import torch
import numpy as np
from models.losses import FocalLoss
from models.losses import RegL1Loss, RegLoss, NormRegL1Loss, RegWeightedL1Loss
from models.decode import ctdet_decode
from models.utils import _sigmoid
from utils.debugger import Debugger
from utils.post_process import ctdet_post_process
from utils.oracle_utils import gen_oracle_map
from .base_trainer import BaseTrainer


def __init__(self, opt):
    super(CtdetLoss, self).__init__()
    self.crit = (torch.nn.MSELoss() if opt.mse_loss else FocalLoss())
    self.crit_reg = (RegL1Loss() if (opt.reg_loss == 'l1') else (RegLoss() if (opt.reg_loss == 'sl1') else None))
    self.crit_wh = (torch.nn.L1Loss(reduction='sum') if opt.dense_wh else (NormRegL1Loss() if opt.norm_wh else (RegWeightedL1Loss() if opt.cat_spec_wh else self.crit_reg)))
    self.opt = opt
