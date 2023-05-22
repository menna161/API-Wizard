import torch
import torch.nn as nn
import torch.nn.parallel
from torch.autograd import Variable
from torchvision import models
import torch.utils.model_zoo as model_zoo
import torch.nn.functional as F
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
from miscc.config import cfg
from GlobalAttention import GlobalAttentionGeneral as ATT_NET


def define_module(self):
    (nz, ngf) = (self.in_dim, self.gf_dim)
    linput = (100 + 81)
    self.ef_dim = 100
    self.bbox_net = BBOX_NET()
    nz += 48
    self.fc = nn.Sequential(nn.Linear(nz, (((ngf * 4) * 4) * 2), bias=False), nn.BatchNorm1d((((ngf * 4) * 4) * 2)), GLU())
    self.label = nn.Sequential(nn.Linear(linput, self.ef_dim, bias=False), nn.BatchNorm1d(self.ef_dim), nn.ReLU(True))
    self.local1 = upBlock(self.ef_dim, (ngf // 2))
    self.local2 = upBlock((ngf // 2), (ngf // 4))
    self.upsample1 = upBlock(ngf, (ngf // 2))
    self.upsample2 = upBlock((ngf // 2), (ngf // 4))
    self.upsample3 = upBlock((ngf // 2), (ngf // 8))
    self.upsample4 = upBlock((ngf // 8), (ngf // 16))
