import torch
import torch.nn as nn


def __init__(self, in_features, out_features, bnorm=True, activation=nn.ReLU(), dropout=None):
    super(GCN_Layer, self).__init__()
    self.bnorm = bnorm
    fc = [nn.Linear(in_features, out_features)]
    if bnorm:
        fc.append(BatchNorm_GCN(out_features))
    if (activation is not None):
        fc.append(activation)
    if (dropout is not None):
        fc.append(nn.Dropout(dropout))
    self.fc = nn.Sequential(*fc)
