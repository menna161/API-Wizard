import torch
import torch.nn as nn
import torch.nn.parallel
from miscc.config import cfg
from miscc.utils import compute_transformation_matrix, compute_transformation_matrix_inverse
from torch.autograd import Variable


def define_module(self):
    (ndf, nef) = (self.df_dim, self.ef_dim)
    self.local = nn.Sequential(nn.Conv2d((3 + 81), (ndf * 2), 4, 1, 1, bias=False), nn.BatchNorm2d((ndf * 2)), nn.LeakyReLU(0.2, inplace=True), nn.Conv2d((ndf * 2), (ndf * 2), 4, 1, 1, bias=False), nn.BatchNorm2d((ndf * 2)), nn.LeakyReLU(0.2, inplace=True))
    self.act = nn.LeakyReLU(0.2, inplace=True)
    self.conv1 = nn.Conv2d(3, ndf, 4, 2, 1, bias=False)
    self.conv2 = nn.Conv2d(ndf, (ndf * 2), 4, 2, 1, bias=False)
    self.bn2 = nn.BatchNorm2d((ndf * 2))
    self.conv3 = nn.Conv2d((ndf * 2), (ndf * 4), 4, 2, 1, bias=False)
    self.bn3 = nn.BatchNorm2d((ndf * 4))
    self.conv4 = nn.Conv2d((ndf * 6), (ndf * 8), 4, 2, 1, bias=False)
    self.bn4 = nn.BatchNorm2d((ndf * 8))
    self.conv5 = nn.Conv2d((ndf * 8), (ndf * 16), 4, 2, 1, bias=False)
    self.bn5 = nn.BatchNorm2d((ndf * 16))
    self.conv6 = nn.Conv2d((ndf * 16), (ndf * 32), 4, 2, 1, bias=False)
    self.bn6 = nn.BatchNorm2d((ndf * 32))
    self.conv7 = conv3x3((ndf * 32), (ndf * 16))
    self.bn7 = nn.BatchNorm2d((ndf * 16))
    self.conv8 = conv3x3((ndf * 16), (ndf * 8))
    self.bn8 = nn.BatchNorm2d((ndf * 8))
    self.get_cond_logits = D_GET_LOGITS(ndf, nef, bcondition=True)
    self.get_uncond_logits = D_GET_LOGITS(ndf, nef, bcondition=False)
