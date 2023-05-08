import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, dim):
    super(Attention, self).__init__()
    self.linear_out = nn.Linear((dim * 2), dim)
    self.mask = None
