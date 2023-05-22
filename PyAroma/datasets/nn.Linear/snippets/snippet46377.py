import torch
import torch.nn as nn
import torch.nn.functional as F


def __init__(self, n_in, n_hid, n_out, do_prob=0.5, out_act=True):
    super().__init__()
    self.fc1 = nn.Linear(n_in, n_hid)
    self.fc2 = nn.Linear((n_hid + n_in), n_out)
    self.bn = nn.BatchNorm1d(n_out)
    self.dropout = nn.Dropout(p=do_prob)
    self.leaky_relu = nn.LeakyReLU(negative_slope=0.01)
    self.init_weights()
    self.out_act = out_act
