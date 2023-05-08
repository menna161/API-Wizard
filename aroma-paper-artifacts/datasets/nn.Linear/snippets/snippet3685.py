import torch
from torch import nn
import numpy as np
from modeling_rel.word_vecs import obj_edge_vectors
from core.config import cfg
import torch.nn.functional as F
from torch.autograd import Variable


def __init__(self, input_dims):
    super(Message_Passing4OBJ, self).__init__()
    self.input_dims = input_dims
    self.trans = nn.Sequential(nn.Linear(self.input_dims, (input_dims // 4)), nn.LayerNorm((self.input_dims // 4)), nn.ReLU(), nn.Linear((self.input_dims // 4), self.input_dims))
    self.get_atten_tensor = Get_Atten_map_mc(self.input_dims, p=1)
    self.conv = nn.Sequential(nn.Linear(self.input_dims, (self.input_dims // 2)), nn.ReLU())
