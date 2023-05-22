import torch
import torch.nn as nn
import torch.nn.functional as F
import copy


def __init__(self, in_dim, out_dim):
    super(linlayer, self).__init__()
    self.in_dim = in_dim
    self.out_dim = out_dim
    self.lin = nn.Linear(in_dim, out_dim)
    self.bn = nn.BatchNorm1d(out_dim)
