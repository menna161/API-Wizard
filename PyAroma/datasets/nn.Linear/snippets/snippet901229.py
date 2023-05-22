import torch
import torch.nn as nn
from onqg.models.modules.SubLayers import MultiHeadAttention, PositionwiseFeedForward, Propagator
from onqg.models.modules.Attention import GatedSelfAttention, GraphAttention
import onqg.dataset.Constants as Constants


def __init__(self, d_hidden, d_model, alpha, feature=False, dropout=0.1, attn_dropout=0.1):
    super(GraphEncoderLayer, self).__init__()
    self.d_hidden = d_hidden
    self.d_model = d_model
    self.feature = feature
    self.edge_num = 3
    bias_list = [False, False, False]
    self.edge_in_list = nn.ModuleList([nn.Linear(d_hidden, d_model, bias=bias_list[i]) for i in range(self.edge_num)])
    self.edge_out_list = nn.ModuleList([nn.Linear(d_hidden, d_model, bias=bias_list[i]) for i in range(self.edge_num)])
    self.graph_in_attention = GraphAttention(d_hidden, d_model, alpha, dropout=attn_dropout)
    self.graph_out_attention = GraphAttention(d_hidden, d_model, alpha, dropout=attn_dropout)
    self.output_gate = Propagator(d_model, dropout=dropout)
