import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from torch.distributions.categorical import Categorical
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
import babyai.rl
from babyai.rl.utils.supervised_losses import required_heads


def __init__(self, in_features, out_features, in_channels, imm_channels):
    super().__init__()
    self.conv1 = nn.Conv2d(in_channels=in_channels, out_channels=imm_channels, kernel_size=(3, 3), padding=1)
    self.bn1 = nn.BatchNorm2d(imm_channels)
    self.conv2 = nn.Conv2d(in_channels=imm_channels, out_channels=out_features, kernel_size=(3, 3), padding=1)
    self.bn2 = nn.BatchNorm2d(out_features)
    self.weight = nn.Linear(in_features, out_features)
    self.bias = nn.Linear(in_features, out_features)
    self.apply(initialize_parameters)
