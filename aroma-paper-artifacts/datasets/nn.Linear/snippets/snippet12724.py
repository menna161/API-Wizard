import torch
import torch.nn as nn
import torch.nn.functional as F
from vocoder.distribution import sample_from_discretized_mix_logistic
from vocoder.display import *
from vocoder.audio import *


def __init__(self, rnn_dims, fc_dims, bits, pad, upsample_factors, feat_dims, compute_dims, res_out_dims, res_blocks, hop_length, sample_rate, mode='RAW'):
    super().__init__()
    self.mode = mode
    self.pad = pad
    if (self.mode == 'RAW'):
        self.n_classes = (2 ** bits)
    elif (self.mode == 'MOL'):
        self.n_classes = 30
    else:
        RuntimeError('Unknown model mode value - ', self.mode)
    self.rnn_dims = rnn_dims
    self.aux_dims = (res_out_dims // 4)
    self.hop_length = hop_length
    self.sample_rate = sample_rate
    self.upsample = UpsampleNetwork(feat_dims, upsample_factors, compute_dims, res_blocks, res_out_dims, pad)
    self.I = nn.Linear(((feat_dims + self.aux_dims) + 1), rnn_dims)
    self.rnn1 = nn.GRU(rnn_dims, rnn_dims, batch_first=True)
    self.rnn2 = nn.GRU((rnn_dims + self.aux_dims), rnn_dims, batch_first=True)
    self.fc1 = nn.Linear((rnn_dims + self.aux_dims), fc_dims)
    self.fc2 = nn.Linear((fc_dims + self.aux_dims), fc_dims)
    self.fc3 = nn.Linear(fc_dims, self.n_classes)
    self.step = nn.Parameter(torch.zeros(1).long(), requires_grad=False)
    self.num_params()
