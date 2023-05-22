import torch
import torch.nn as nn
from torch.nn.parallel import data_parallel
import numpy as np
import dgl.function as fn
from torch.nn.init import xavier_normal_, xavier_uniform_
from torch.nn import functional as F, Parameter


def __init__(self, in_feat, out_feat, num_rels, num_bases, bias=True, activation=None, self_loop=False, dropout=0.2):
    super(GATLayer, self).__init__(in_feat, out_feat, bias, activation, self_loop=self_loop, dropout=dropout)
    self.in_feat = in_feat
    self.out_feat = out_feat
    self.weight = nn.Linear(in_feat, out_feat, bias=False)
    self.weight_rel = torch.nn.Embedding(num_rels, 1, padding_idx=0)
    self.attn_fc = nn.Linear((2 * out_feat), 1, bias=False)
