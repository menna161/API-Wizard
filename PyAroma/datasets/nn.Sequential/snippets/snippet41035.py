import torch
import torch.nn as nn
import torch.nn.parallel
from miscc.config import cfg
from miscc.utils import compute_transformation_matrix, compute_transformation_matrix_inverse
from torch.autograd import Variable


def __init__(self, ndf, nef, bcondition=True):
    super(D_GET_LOGITS, self).__init__()
    self.df_dim = ndf
    self.ef_dim = cfg.GAN.CONDITION_DIM
    self.bcondition = bcondition
    if bcondition:
        self.outlogits = nn.Sequential(conv3x3(((ndf * 8) + 13), (ndf * 8)), nn.BatchNorm2d((ndf * 8)), nn.LeakyReLU(0.2, inplace=True), nn.Conv2d((ndf * 8), 1, kernel_size=4, stride=4))
    else:
        self.outlogits = nn.Sequential(nn.Conv2d(109, 1, kernel_size=4, stride=4))
