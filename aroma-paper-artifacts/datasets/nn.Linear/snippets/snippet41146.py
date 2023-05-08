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
    super(CA_NET, self).__init__()
    self.t_dim = cfg.TEXT.EMBEDDING_DIM
    self.c_dim = cfg.GAN.CONDITION_DIM
    self.fc = nn.Linear(self.t_dim, (self.c_dim * 4), bias=True)
    self.relu = GLU()
