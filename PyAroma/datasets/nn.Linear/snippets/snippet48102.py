from collections import OrderedDict
import torch
import torch.nn as nn


def __init__(self, l, fan_in, fan_out, batch_norm=1e-05, dropout=0.0):
    super(SingleLinearLayer, self).__init__()
    self.fclayer = nn.Sequential(OrderedDict([(('fc' + str(l)), nn.Linear(fan_in, fan_out, bias=False))]))
    if (batch_norm > 0.0):
        self.fclayer.add_module(('bn' + str(l)), nn.BatchNorm1d(fan_out, eps=batch_norm))
    self.fclayer.add_module(('act' + str(l)), nn.ReLU())
    if (not (dropout == 0.0)):
        self.fclayer.add_module('dropout', nn.Dropout2d(p=dropout, inplace=False))
