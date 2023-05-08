import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


def __init__(self, dim_neck, dim_emb, dim_pre):
    super(Decoder, self).__init__()
    self.conv1 = nn.Sequential(ConvNorm(((dim_neck * 2) + dim_emb), dim_pre, kernel_size=5, stride=1, padding=2, dilation=1, w_init_gain='relu'), nn.BatchNorm1d(dim_pre))
    convolutions = []
    for i in range(2):
        conv_layer = nn.Sequential(ConvNorm(dim_pre, dim_pre, kernel_size=5, stride=1, padding=2, dilation=1, w_init_gain='relu'), nn.BatchNorm1d(dim_pre))
        convolutions.append(conv_layer)
    self.convolutions = nn.ModuleList(convolutions)
    self.lstm = nn.LSTM(dim_pre, 1024, 3, batch_first=True)
    self.linear_projection = LinearNorm(1024, 80)
