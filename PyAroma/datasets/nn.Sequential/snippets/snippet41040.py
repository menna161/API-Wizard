import torch
import torch.nn as nn
import torch.nn.parallel
from miscc.config import cfg
from miscc.utils import compute_transformation_matrix, compute_transformation_matrix_inverse
from torch.autograd import Variable


def define_module(self):
    ninput = self.z_dim
    linput = 13
    ngf = self.gf_dim
    if (cfg.USE_BBOX_LAYOUT or cfg.USE_BBOX_LAYOUT_S1):
        self.bbox_net = BBOX_NET()
        ninput += 8
    self.fc = nn.Sequential(nn.Linear(ninput, ((ngf * 4) * 4), bias=False), nn.BatchNorm1d(((ngf * 4) * 4)), nn.ReLU(True))
    self.label = nn.Sequential(nn.Linear(linput, self.ef_dim, bias=False), nn.BatchNorm1d(self.ef_dim), nn.ReLU(True))
    self.local1 = upBlock(self.ef_dim, (ngf // 2))
    self.local2 = upBlock((ngf // 2), (ngf // 4))
    self.upsample1 = upBlock(ngf, (ngf // 2))
    self.upsample2 = upBlock((ngf // 2), (ngf // 4))
    self.upsample3 = upBlock((ngf // 2), (ngf // 8))
    self.upsample4 = upBlock((ngf // 8), (ngf // 16))
    self.img = nn.Sequential(conv3x3((ngf // 16), 3), nn.Tanh())
