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


def __init__(self, channel_num):
    super(ResBlock, self).__init__()
    self.block = nn.Sequential(conv3x3(channel_num, (channel_num * 2)), nn.BatchNorm2d((channel_num * 2)), GLU(), conv3x3(channel_num, channel_num), nn.BatchNorm2d(channel_num))
