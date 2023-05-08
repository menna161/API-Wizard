import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


def __init__(self, dim_neck, dim_emb, freq):
    super(Encoder, self).__init__()
    self.dim_neck = dim_neck
    self.freq = freq
    convolutions = []
    for i in range(3):
        conv_layer = nn.Sequential(ConvNorm(((80 + dim_emb) if (i == 0) else 512), 512, kernel_size=5, stride=1, padding=2, dilation=1, w_init_gain='relu'), nn.BatchNorm1d(512))
        convolutions.append(conv_layer)
    self.convolutions = nn.ModuleList(convolutions)
    self.lstm = nn.LSTM(512, dim_neck, 2, batch_first=True, bidirectional=True)
