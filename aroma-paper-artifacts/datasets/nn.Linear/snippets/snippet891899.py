import os
import copy
import json
import math
import logging
import tarfile
import tempfile
import shutil
import collections
import sys
from io import open
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn import CrossEntropyLoss
from torch.nn.parameter import Parameter
from .modeling import BertLayerNorm as LayerNorm
from .modeling_transfo_xl_utilities import ProjectedAdaptiveLogSoftmax, sample_logits
from .file_utils import cached_path
import numpy as np
import tensorflow as tf


def __init__(self, n_head, d_model, d_head, dropout, dropatt=0, pre_lnorm=False, r_r_bias=None, r_w_bias=None):
    super(MultiHeadAttn, self).__init__()
    self.n_head = n_head
    self.d_model = d_model
    self.d_head = d_head
    self.dropout = dropout
    self.q_net = nn.Linear(d_model, (n_head * d_head), bias=False)
    self.kv_net = nn.Linear(d_model, ((2 * n_head) * d_head), bias=False)
    self.drop = nn.Dropout(dropout)
    self.dropatt = nn.Dropout(dropatt)
    self.o_net = nn.Linear((n_head * d_head), d_model, bias=False)
    self.layer_norm = LayerNorm(d_model)
    self.scale = (1 / (d_head ** 0.5))
    self.pre_lnorm = pre_lnorm
    if ((r_r_bias is None) or (r_w_bias is None)):
        self.r_r_bias = nn.Parameter(torch.Tensor(self.n_head, self.d_head))
        self.r_w_bias = nn.Parameter(torch.Tensor(self.n_head, self.d_head))
    else:
        self.r_r_bias = r_r_bias
        self.r_w_bias = r_w_bias
