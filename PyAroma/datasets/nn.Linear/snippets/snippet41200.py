import torch
import torch.nn as nn
import torch.nn.parallel
from miscc.config import cfg
from miscc.utils import compute_transformation_matrix, compute_transformation_matrix_inverse
from torch.autograd import Variable


def __init__(self):
    super(CA_NET, self).__init__()
    self.t_dim = cfg.TEXT.DIMENSION
    self.c_dim = cfg.GAN.CONDITION_DIM
    self.fc = nn.Linear(self.t_dim, (self.c_dim * 2), bias=True)
    self.relu = nn.ReLU()
