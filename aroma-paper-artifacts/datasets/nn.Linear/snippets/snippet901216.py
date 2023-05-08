import torch
import torch.nn as nn
import numpy as np
import math


def __init__(self, attend_dim, query_dim, att_dim, is_coverage=False):
    super(ConcatAttention, self).__init__()
    self.attend_dim = attend_dim
    self.query_dim = query_dim
    self.att_dim = att_dim
    self.linear_pre = nn.Linear(attend_dim, att_dim, bias=True)
    self.linear_q = nn.Linear(query_dim, att_dim, bias=False)
    self.linear_v = nn.Linear(att_dim, 1, bias=False)
    self.sftmax = nn.Softmax(dim=1)
    self.tanh = nn.Tanh()
    self.mask = None
    self.is_coverage = is_coverage
    if is_coverage:
        self.linear_cov = nn.Linear(1, att_dim, bias=False)
