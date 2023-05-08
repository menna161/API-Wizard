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


def __init__(self, input_dims, output_dims):
    super().__init__()
    self.Ws = nn.Sequential(nn.Linear(input_dims, (output_dims * 2)), nn.ReLU(inplace=True), nn.Linear((output_dims * 2), output_dims))
    self.Wo = nn.Sequential(nn.Linear(input_dims, (output_dims * 2)), nn.ReLU(inplace=True), nn.Linear((output_dims * 2), output_dims))
