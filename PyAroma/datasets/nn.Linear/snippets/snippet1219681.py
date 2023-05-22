import torch
from torch import nn
from torch.nn import functional as F
from torch.distributions.normal import Normal
from lib.utils.vis_logger import logger


def __init__(self, dim_in, dim_h, dim_out, act):
    nn.Module.__init__(self)
    self.dim_in = dim_in
    self.dim_out = dim_out
    self.fc1 = nn.Linear(dim_in, dim_h)
    self.fc2 = nn.Linear(dim_h, dim_out)
    self.act = act
