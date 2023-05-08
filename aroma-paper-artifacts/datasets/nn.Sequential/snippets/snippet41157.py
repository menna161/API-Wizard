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


def __init__(self, ngf):
    super(GET_IMAGE_G, self).__init__()
    self.gf_dim = ngf
    self.img = nn.Sequential(conv3x3(ngf, 3), nn.Tanh())
