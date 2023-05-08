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


def Block3x3_leakRelu(in_planes, out_planes):
    block = nn.Sequential(conv3x3(in_planes, out_planes), nn.BatchNorm2d(out_planes), nn.LeakyReLU(0.2, inplace=True))
    return block
