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


def _make_layer(self, block, channel_num):
    layers = []
    for i in range(cfg.GAN.R_NUM):
        layers.append(block(channel_num))
    return nn.Sequential(*layers)
