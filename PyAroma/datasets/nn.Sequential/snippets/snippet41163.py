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


def __init__(self, ndf, nef, bcondition=False):
    super(D_GET_LOGITS, self).__init__()
    self.df_dim = ndf
    self.ef_dim = nef
    self.bcondition = bcondition
    if self.bcondition:
        self.jointConv = Block3x3_leakRelu(((ndf * 8) + nef), (ndf * 8))
    self.outlogits = nn.Sequential(nn.Conv2d((ndf * 8), 1, kernel_size=4, stride=4), nn.Sigmoid())
