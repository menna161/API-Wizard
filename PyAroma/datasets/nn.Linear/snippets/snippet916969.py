import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.utils import weight_norm as wn


def __init__(self, dim_in, dim_out):
    super(nin, self).__init__()
    self.lin_a = wn(nn.Linear(dim_in, dim_out))
    self.dim_out = dim_out
