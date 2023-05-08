import torch
import math
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter
from torch.nn.init import xavier_normal_


def __init__(self, num_entities, num_relations, args):
    super(ConvE, self).__init__()
    self.w_relation = torch.nn.Embedding(num_relations, args.n_hidden, padding_idx=0)
    self.inp_drop = torch.nn.Dropout(args.input_dropout)
    self.hidden_drop = torch.nn.Dropout(args.dropout)
    self.feature_map_drop = torch.nn.Dropout2d(args.feature_map_dropout)
    self.conv1 = torch.nn.Conv2d(1, 32, (3, 3), 1, 0, bias=args.use_bias)
    self.bn0 = torch.nn.BatchNorm2d(1)
    self.bn1 = torch.nn.BatchNorm2d(32)
    self.bn2 = torch.nn.BatchNorm1d(args.n_hidden)
    self.register_parameter('b', Parameter(torch.zeros(num_entities)))
    self.fc = torch.nn.Linear(10368, args.n_hidden)
