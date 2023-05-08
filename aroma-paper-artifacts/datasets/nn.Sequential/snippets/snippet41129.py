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


def downBlock(in_planes, out_planes):
    block = nn.Sequential(nn.Conv2d(in_planes, out_planes, 4, 2, 1, bias=False), nn.BatchNorm2d(out_planes), nn.LeakyReLU(0.2, inplace=True))
    return block
