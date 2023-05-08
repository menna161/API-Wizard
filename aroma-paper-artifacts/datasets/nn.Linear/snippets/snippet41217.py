import torch
import torch.nn as nn
import torch.nn.parallel
from miscc.config import cfg
from miscc.utils import compute_transformation_matrix, compute_transformation_matrix_inverse
from torch.autograd import Variable


def define_module(self):
    ngf = self.gf_dim
    self.ca_net = CA_NET()
    linput = (self.ef_dim + 81)
    self.label = nn.Sequential(nn.Linear(linput, self.ef_dim, bias=False), nn.BatchNorm1d(self.ef_dim), nn.ReLU(True))
    self.local1 = upBlock((self.ef_dim + 768), (ngf * 2))
    self.local2 = upBlock((ngf * 2), ngf)
    self.encoder = nn.Sequential(conv3x3(3, ngf), nn.ReLU(True), nn.Conv2d(ngf, (ngf * 2), 4, 2, 1, bias=False), nn.BatchNorm2d((ngf * 2)), nn.ReLU(True), nn.Conv2d((ngf * 2), (ngf * 4), 4, 2, 1, bias=False), nn.BatchNorm2d((ngf * 4)), nn.ReLU(True))
    if cfg.USE_BBOX_LAYOUT:
        self.hr_joint = nn.Sequential(conv3x3(((self.ef_dim * 2) + (ngf * 4)), (ngf * 4)), nn.BatchNorm2d((ngf * 4)), nn.ReLU(True))
    else:
        self.hr_joint = nn.Sequential(conv3x3((self.ef_dim + (ngf * 4)), (ngf * 4)), nn.BatchNorm2d((ngf * 4)), nn.ReLU(True))
    self.residual = self._make_layer(ResBlock, (ngf * 4))
    self.upsample1 = upBlock((ngf * 4), (ngf * 2))
    self.upsample2 = upBlock((ngf * 2), ngf)
    self.upsample3 = upBlock((ngf * 2), (ngf // 2))
    self.upsample4 = upBlock((ngf // 2), (ngf // 4))
    self.img = nn.Sequential(conv3x3((ngf // 4), 3), nn.Tanh())
