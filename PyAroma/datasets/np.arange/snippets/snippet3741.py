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


def diagonal_inds(array):
    '\n    Returns the indices required to go along first 2 dims of tensor in diag fashion\n    :param tensor: thing\n    :return: \n    '
    assert (len(array.shape) >= 2)
    assert (array.shape[0] == array.shape[1])
    size = array.shape[0]
    arange_inds = np.arange(0, size, dtype=np.int64)
    return ((size + 1) * arange_inds)
