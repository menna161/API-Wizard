import sys
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable


def __init__(self, dec_type, input_size, output_size, hidden_size, d_size, n_layer=1, dropout=0.5):
    super(DecoderDeep, self).__init__()
    self.dec_type = dec_type
    self.input_size = input_size
    self.hidden_size = hidden_size
    self.output_size = output_size
    self.d_size = d_size
    self.n_layer = n_layer
    self.dropout = dropout
    print('Using sclstm as decoder with module list!')
    assert (d_size != None)
    (self.w2h, self.h2h) = (nn.ModuleList(), nn.ModuleList())
    (self.w2h_r, self.h2h_r) = (nn.ModuleList(), nn.ModuleList())
    self.dc = nn.ModuleList()
    for i in range(n_layer):
        if (i == 0):
            self.w2h.append(nn.Linear(input_size, (hidden_size * 4)).cuda())
            self.w2h_r.append(nn.Linear(input_size, d_size).cuda())
        else:
            self.w2h.append(nn.Linear((input_size + (i * hidden_size)), (hidden_size * 4)).cuda())
            self.w2h_r.append(nn.Linear((input_size + (i * hidden_size)), d_size).cuda())
        self.h2h.append(nn.Linear(hidden_size, (hidden_size * 4)).cuda())
        self.h2h_r.append(nn.Linear(hidden_size, d_size).cuda())
        self.dc.append(nn.Linear(d_size, hidden_size, bias=False).cuda())
    self.out = nn.Linear((hidden_size * n_layer), output_size)
