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


def __init__(self):
    super(BBOX_NET, self).__init__()
    self.c_dim = cfg.GAN.CONDITION_DIM
    self.encode = nn.Sequential(conv3x3(self.c_dim, (self.c_dim // 2), stride=2), nn.LeakyReLU(0.2, inplace=True), conv3x3((self.c_dim // 2), (self.c_dim // 4), stride=2), nn.BatchNorm2d((self.c_dim // 4)), nn.LeakyReLU(0.2, inplace=True), conv3x3((self.c_dim // 4), (self.c_dim // 8), stride=2), nn.BatchNorm2d((self.c_dim // 8)), nn.LeakyReLU(0.2, inplace=True))
