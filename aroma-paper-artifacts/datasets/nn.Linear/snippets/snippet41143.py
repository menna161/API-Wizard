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


def define_module(self, model):
    self.Conv2d_1a_3x3 = model.Conv2d_1a_3x3
    self.Conv2d_2a_3x3 = model.Conv2d_2a_3x3
    self.Conv2d_2b_3x3 = model.Conv2d_2b_3x3
    self.Conv2d_3b_1x1 = model.Conv2d_3b_1x1
    self.Conv2d_4a_3x3 = model.Conv2d_4a_3x3
    self.Mixed_5b = model.Mixed_5b
    self.Mixed_5c = model.Mixed_5c
    self.Mixed_5d = model.Mixed_5d
    self.Mixed_6a = model.Mixed_6a
    self.Mixed_6b = model.Mixed_6b
    self.Mixed_6c = model.Mixed_6c
    self.Mixed_6d = model.Mixed_6d
    self.Mixed_6e = model.Mixed_6e
    self.Mixed_7a = model.Mixed_7a
    self.Mixed_7b = model.Mixed_7b
    self.Mixed_7c = model.Mixed_7c
    self.emb_features = conv1x1(768, self.nef)
    self.emb_cnn_code = nn.Linear(2048, self.nef)
