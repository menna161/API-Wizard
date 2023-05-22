import torch
import torch.nn as nn
import torch.nn.functional as F
from net.utils.graph import Graph_J, Graph_P, Graph_B
from net.utils.module import *
from net.utils.operation import PartLocalInform, BodyLocalInform


def __init__(self, n_in_dec, n_hid_dec, graph_args_j, edge_weighting=True, dropout=0.3, **kwargs):
    super().__init__()
    self.graph_j = Graph_J(**graph_args_j)
    A_j = torch.tensor(self.graph_j.A_j, dtype=torch.float32, requires_grad=False)
    self.register_buffer('A_j', A_j)
    (k_num, self.V) = (self.A_j.size(0), self.A_j.size(1))
    if edge_weighting:
        self.emul = nn.Parameter(torch.ones(self.A_j.size()))
        self.eadd = nn.Parameter(torch.ones(self.A_j.size()))
    else:
        self.emul = 1
        self.eadd = nn.Parameter(torch.ones(self.A_j.size()))
    self.msg_in = DecodeGcn(n_hid_dec, n_hid_dec, k_num)
    self.input_r = nn.Linear(n_in_dec, n_hid_dec, bias=True)
    self.input_i = nn.Linear(n_in_dec, n_hid_dec, bias=True)
    self.input_n = nn.Linear(n_in_dec, n_hid_dec, bias=True)
    self.hidden_r = nn.Linear(n_hid_dec, n_hid_dec, bias=False)
    self.hidden_i = nn.Linear(n_hid_dec, n_hid_dec, bias=False)
    self.hidden_h = nn.Linear(n_hid_dec, n_hid_dec, bias=False)
    self.out_fc1 = nn.Linear(n_hid_dec, n_hid_dec)
    self.out_fc2 = nn.Linear(n_hid_dec, n_hid_dec)
    self.out_fc3 = nn.Linear(n_hid_dec, 3)
    self.dropout1 = nn.Dropout(dropout)
    self.dropout2 = nn.Dropout(dropout)
    self.relu = nn.ReLU()
    self.leaky_relu = nn.LeakyReLU(negative_slope=0.1)
    self.mask = torch.ones(78).cuda().detach()
    self.zero_idx = torch.tensor([5, 11, 17, 23, 45, 49, 50, 54, 55, 63, 67, 68, 72, 73]).cuda().detach()
    self.mask[self.zero_idx] = 0.0
