from typing import Dict, Iterator, List
import torch
import torch.nn as nn
from torch.autograd import Variable
from allennlp.modules.text_field_embedders import TextFieldEmbedder
from allennlp.modules.matrix_attention.cosine_matrix_attention import CosineMatrixAttention
from allennlp.modules.matrix_attention.dot_product_matrix_attention import *
import math


def __init__(self, _embsize: int, kernels_mu: List[float], kernels_sigma: List[float], att_heads: int, att_layer: int, att_ff_dim: int, max_length, use_pos_encoding, use_diff_posencoding, saturation_type):
    super(TKL_sigir20, self).__init__()
    n_kernels = len(kernels_mu)
    self.use_pos_encoding = use_pos_encoding
    self.use_diff_posencoding = use_diff_posencoding
    self.re_use_encoding = True
    self.chunk_size = 40
    self.overlap = 5
    self.extended_chunk_size = (self.chunk_size + (2 * self.overlap))
    self.sliding_window_size = 30
    self.top_k_chunks = 3
    self.use_idf_sat = (saturation_type == 'idf')
    self.use_embedding_sat = (saturation_type == 'embedding')
    self.use_linear_sat = (saturation_type == 'linear')
    self.use_log_sat = (saturation_type == 'log')
    if (len(kernels_mu) != len(kernels_sigma)):
        raise Exception('len(kernels_mu) != len(kernels_sigma)')
    self.mu = nn.Parameter(torch.cuda.FloatTensor(kernels_mu), requires_grad=False)
    self.sigma = nn.Parameter(torch.cuda.FloatTensor(kernels_sigma), requires_grad=False)
    pos_f = self.get_positional_features(_embsize, 30)
    pos_f.requires_grad = True
    self.positional_features_q = nn.Parameter(pos_f)
    self.positional_features_q.requires_grad = True
    if (self.use_diff_posencoding == True):
        pos_f = self.get_positional_features(_embsize, ((2000 + 500) + self.extended_chunk_size))[(:, 500:, :)].clone()
        pos_f.requires_grad = True
        self.positional_features_d = nn.Parameter(pos_f)
        self.positional_features_d.requires_grad = True
    else:
        self.positional_features_d = self.positional_features_q
    self.mixer = nn.Parameter(torch.full([1], 0.5, dtype=torch.float32, requires_grad=True))
    self.mixer_sat = nn.Parameter(torch.full([1], 0.5, dtype=torch.float32, requires_grad=True))
    encoder_layer = nn.TransformerEncoderLayer(_embsize, att_heads, dim_feedforward=att_ff_dim, dropout=0)
    self.contextualizer = nn.TransformerEncoder(encoder_layer, att_layer, norm=None)
    self.cosine_module = CosineMatrixAttention()
    self.saturation_linear = nn.Linear(2, 1, bias=True)
    torch.nn.init.constant_(self.saturation_linear.bias, 100)
    torch.nn.init.uniform_(self.saturation_linear.weight, (- 0.014), 0.014)
    self.saturation_linear2 = nn.Linear(2, 1, bias=True)
    torch.nn.init.constant_(self.saturation_linear2.bias, 100)
    torch.nn.init.uniform_(self.saturation_linear2.weight, (- 0.014), 0.014)
    self.saturation_linear3 = nn.Linear(2, 1, bias=True)
    torch.nn.init.constant_(self.saturation_linear3.bias, 100)
    torch.nn.init.uniform_(self.saturation_linear3.weight, (- 0.014), 0.014)
    self.sat_normer = nn.LayerNorm(2, elementwise_affine=True)
    self.sat_emb_reduce1 = nn.Linear(_embsize, 1, bias=False)
    self.kernel_mult = nn.Parameter(torch.full([4, 1, 1, 1, n_kernels], 1, dtype=torch.float32, requires_grad=True))
    self.chunk_scoring = nn.Parameter(torch.full([1, (self.top_k_chunks * 5)], 1, dtype=torch.float32, requires_grad=True))
    self.mixer_end = nn.Parameter(torch.full([1], 0.5, dtype=torch.float32, requires_grad=True))
    self.dense = nn.Linear(n_kernels, 1, bias=False)
    torch.nn.init.uniform_(self.dense.weight, (- 0.014), 0.014)
