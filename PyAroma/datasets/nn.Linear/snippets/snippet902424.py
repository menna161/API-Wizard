import torch
import math
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parameter import Parameter
from torch.nn.init import xavier_normal_


def __init__(self, num_entities, num_relations, args):
    '\n        Difference from ConvE: no reshaping after stacking e_1 and e_r\n        '
    super(ConvTransE, self).__init__()
    bert_dims = 1024
    self.no_cuda = args.no_cuda
    if (args.bert_concat or args.tying):
        emb_dim = (args.embedding_dim + bert_dims)
    elif args.bert_mlp:
        emb_dim = 600
    else:
        emb_dim = args.embedding_dim
    if (args.gcn_type == 'MultiHeadGATLayer'):
        num_heads = 8
        emb_dim = ((args.embedding_dim * num_heads) + bert_dims)
    self.embedding_dim = emb_dim
    self.w_relation = torch.nn.Embedding(num_relations, emb_dim, padding_idx=0)
    self.inp_drop = torch.nn.Dropout(args.input_dropout)
    self.hidden_drop = torch.nn.Dropout(args.dropout)
    self.feature_map_drop = torch.nn.Dropout(args.feature_map_dropout)
    kernel_size = 5
    self.channels = 200
    self.conv1 = nn.Conv1d(2, self.channels, kernel_size, stride=1, padding=int(math.floor((kernel_size / 2))))
    self.bn0 = torch.nn.BatchNorm1d(2)
    self.bn1 = torch.nn.BatchNorm1d(self.channels)
    self.bn2 = torch.nn.BatchNorm1d(emb_dim)
    self.fc = torch.nn.Linear((self.channels * emb_dim), emb_dim)
    self.loss = torch.nn.BCELoss()
    self.cur_embedding = None
