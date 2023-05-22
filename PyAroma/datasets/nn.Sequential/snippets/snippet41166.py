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
    self.act = nn.LeakyReLU(0.2, inplace=True)
    ndf = cfg.GAN.DF_DIM
    self.conv1 = nn.Conv2d(3, ndf, 4, 2, 1, bias=False)
    self.conv2 = nn.Conv2d(ndf, (ndf * 2), 4, 2, 1, bias=False)
    self.bn2 = nn.BatchNorm2d((ndf * 2))
    self.conv3 = nn.Conv2d((ndf * 4), (ndf * 4), 4, 2, 1, bias=False)
    self.bn3 = nn.BatchNorm2d((ndf * 4))
    self.conv4 = nn.Conv2d((ndf * 4), (ndf * 8), 4, 2, 1, bias=False)
    self.bn4 = nn.BatchNorm2d((ndf * 8))
    self.local = nn.Sequential(nn.Conv2d((3 + 81), (ndf * 2), 4, 1, 1, bias=False), nn.BatchNorm2d((ndf * 2)), nn.LeakyReLU(0.2, inplace=True))
