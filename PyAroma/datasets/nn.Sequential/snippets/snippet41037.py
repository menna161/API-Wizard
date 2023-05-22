import torch
import torch.nn as nn
import torch.nn.parallel
from miscc.config import cfg
from miscc.utils import compute_transformation_matrix, compute_transformation_matrix_inverse
from torch.autograd import Variable


def __init__(self):
    super(BBOX_NET, self).__init__()
    self.c_dim = cfg.GAN.CONDITION_DIM
    self.encode = nn.Sequential(conv3x3(self.c_dim, (self.c_dim // 2), stride=2), nn.LeakyReLU(0.2, inplace=True), conv3x3((self.c_dim // 2), (self.c_dim // 4), stride=2), nn.BatchNorm2d((self.c_dim // 4)), nn.LeakyReLU(0.2, inplace=True), conv3x3((self.c_dim // 4), (self.c_dim // 8), stride=2), nn.BatchNorm2d((self.c_dim // 8)), nn.LeakyReLU(0.2, inplace=True))
