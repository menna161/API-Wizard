import torch
from torch import nn
from torch.nn import functional as F
from torch.autograd import Variable
import numpy as np


def __init__(self, input_dims):
    super(Direction_Aware_MP, self).__init__()
    self.input_dims = input_dims
    self.trans = nn.Sequential(nn.Linear(self.input_dims, (input_dims // 4)), LayerNorm((self.input_dims // 4)), nn.ReLU(inplace=True), nn.Linear((self.input_dims // 4), self.input_dims))
    self.get_atten_tensor = Get_Atten_map_mc(self.input_dims, p=1)
    self.conv = nn.Sequential(nn.Linear(self.input_dims, (self.input_dims // 2)), nn.ReLU(inplace=True))
