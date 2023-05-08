import torch
from torch import nn
from torch.nn import functional as F
from torch.autograd import Variable
import numpy as np


def __init__(self, input_dims, p):
    super(Get_Atten_map_mc, self).__init__()
    self.input_dims = input_dims
    self.p = p
    self.ws = nn.Linear(input_dims, input_dims)
    self.wo = nn.Linear(input_dims, input_dims)
    self.w = nn.Linear(self.input_dims, self.p)
