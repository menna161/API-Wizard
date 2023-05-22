import torch
from torch import nn
import numpy as np
from modeling_rel.word_vecs import obj_edge_vectors
from core.config import cfg
import torch.nn.functional as F
from torch.autograd import Variable


def __init__(self, input_dims):
    super(GRU, self).__init__()
    self.input_dims = input_dims
    self.w3 = nn.Linear(input_dims, input_dims)
    self.u3 = nn.Linear(input_dims, input_dims)
    self.w4 = nn.Linear(input_dims, input_dims)
    self.u4 = nn.Linear(input_dims, input_dims)
    self.w5 = nn.Linear(input_dims, input_dims)
    self.u5 = nn.Linear(input_dims, input_dims)
