import torch
import math
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter
from torch.nn.init import xavier_normal_


def __init__(self, num_entities, num_relations, args):
    super(ConvKB, self).__init__()
    self.w_relation = torch.nn.Embedding(num_relations, args.n_hidden, padding_idx=0)
    self.inp_drop = torch.nn.Dropout(args.input_dropout)
    self.hidden_drop = torch.nn.Dropout(args.dropout)
    self.feature_map_drop = torch.nn.Dropout(args.feature_map_dropout)
    self.loss = torch.nn.BCELoss()
    self.conv1 = torch.nn.Conv1d(3, 50, 3, bias=args.use_bias)
    self.bn0 = torch.nn.BatchNorm1d(1)
    self.bn1 = torch.nn.BatchNorm1d(50)
    self.bn2 = torch.nn.BatchNorm1d(1)
    self.fc = torch.nn.Linear(24900, 1)
    print(num_entities, num_relations)
