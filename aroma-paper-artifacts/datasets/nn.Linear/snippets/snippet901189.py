import torch
import torch.nn as nn
from torch.nn.utils.rnn import pad_packed_sequence as unpack
from torch.nn.utils.rnn import pack_padded_sequence as pack
import onqg.dataset.Constants as Constants
from onqg.models.modules.Attention import GatedSelfAttention, ConcatAttention
from onqg.models.modules.Layers import GraphEncoderLayer, SparseGraphEncoderLayer


def __init__(self, n_edge_type, d_model, d_rnn_enc_model, n_layer, alpha, d_feat_vec, feat_vocab, edge_bias, layer_attn, dropout, attn_dropout):
    self.name = 'graph'
    super(SparseGraphEncoder, self).__init__()
    self.layer_attn = layer_attn
    self.hidden_size = d_model
    self.d_model = d_model
    self.feature = (True if feat_vocab else False)
    if self.feature:
        self.feat_embs = nn.ModuleList([nn.Embedding(n_f_vocab, d_feat_vec, padding_idx=Constants.PAD) for n_f_vocab in feat_vocab])
        self.hidden_size += (d_feat_vec * len(feat_vocab))
    self.edge_in_emb = nn.Embedding(n_edge_type, (self.hidden_size * d_model), padding_idx=Constants.PAD)
    self.edge_out_emb = nn.Embedding(n_edge_type, (self.hidden_size * d_model), padding_idx=Constants.PAD)
    self.edge_bias = edge_bias
    if edge_bias:
        self.edge_in_emb_bias = nn.Embedding(n_edge_type, d_model, padding_idx=Constants.PAD)
        self.edge_out_emb_bias = nn.Embedding(n_edge_type, d_model, padding_idx=Constants.PAD)
    self.layer_stack = nn.ModuleList([SparseGraphEncoderLayer(self.hidden_size, d_model, alpha, edge_bias=edge_bias, feature=self.feature, dropout=dropout, attn_dropout=attn_dropout) for _ in range(n_layer)])
    self.gate = nn.Linear((d_model * 2), d_model, bias=False)
