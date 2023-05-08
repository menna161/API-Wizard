import torch
from torch import nn
import numpy as np
from modeling_rel.word_vecs import obj_edge_vectors
from core.config import cfg
import torch.nn.functional as F
from torch.autograd import Variable


def __init__(self, input_dims, p):
    super(Get_Atten_map_mc, self).__init__()
    self.input_dims = input_dims
    self.p = p
    self.ws = nn.Linear(self.input_dims, self.input_dims)
    self.wo = nn.Linear(self.input_dims, self.input_dims)
    self.w = nn.Linear(self.input_dims, self.p)
