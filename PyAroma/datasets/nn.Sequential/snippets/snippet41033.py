import torch
import torch.nn as nn
import torch.nn.parallel
from miscc.config import cfg
from miscc.utils import compute_transformation_matrix, compute_transformation_matrix_inverse
from torch.autograd import Variable


def __init__(self, channel_num):
    super(ResBlock, self).__init__()
    self.block = nn.Sequential(conv3x3(channel_num, channel_num), nn.BatchNorm2d(channel_num), nn.ReLU(True), conv3x3(channel_num, channel_num), nn.BatchNorm2d(channel_num))
    self.relu = nn.ReLU(inplace=True)
