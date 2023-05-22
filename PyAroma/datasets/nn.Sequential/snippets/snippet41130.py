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


def encode_image_by_16times(ndf):
    encode_img = nn.Sequential(nn.Conv2d(3, ndf, 4, 2, 1, bias=False), nn.LeakyReLU(0.2, inplace=True), nn.Conv2d(ndf, (ndf * 2), 4, 2, 1, bias=False), nn.BatchNorm2d((ndf * 2)), nn.LeakyReLU(0.2, inplace=True), nn.Conv2d((ndf * 2), (ndf * 4), 4, 2, 1, bias=False), nn.BatchNorm2d((ndf * 4)), nn.LeakyReLU(0.2, inplace=True), nn.Conv2d((ndf * 4), (ndf * 8), 4, 2, 1, bias=False), nn.BatchNorm2d((ndf * 8)), nn.LeakyReLU(0.2, inplace=True))
    return encode_img
