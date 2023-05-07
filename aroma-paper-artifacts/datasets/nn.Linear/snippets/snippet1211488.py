from typing import Dict, Iterator, List
import torch
import torch.nn as nn
from allennlp.modules.matrix_attention.cosine_matrix_attention import CosineMatrixAttention
import math


def __init__(self, _embsize: int, kernels_mu: List[float], kernels_sigma: List[float], att_heads: int, att_layer: int, att_proj_dim: int, att_ff_dim: int, max_length: int, use_diff_posencoding: bool):
    super(CIKM20_TK_Sparse, self).__init__()
    self.mixer_stop = nn.Parameter(torch.full([1], 0.5, dtype=torch.float32, requires_grad=True))
    self.mixer = nn.Parameter(torch.full([1], 0.5, dtype=torch.float32, requires_grad=True))
    self.use_diff_posencoding = use_diff_posencoding
    self.register_buffer('positional_features_q', self.get_positional_features(_embsize, max_length))
    if (self.use_diff_posencoding == True):
        self.register_buffer('positional_features_d', self.get_positional_features(_embsize, (max_length + 500))[(:, 500:, :)])
    else:
        self.register_buffer('positional_features_d', self.positional_features_q)
    encoder_layer = nn.TransformerEncoderLayer(_embsize, att_heads, dim_feedforward=att_ff_dim, dropout=0)
    self.contextualizer = nn.TransformerEncoder(encoder_layer, att_layer, norm=None)
    self.cosine_module = CosineMatrixAttention()
    n_kernels = len(kernels_mu)
    if (len(kernels_mu) != len(kernels_sigma)):
        raise Exception('len(kernels_mu) != len(kernels_sigma)')
    self.register_buffer('mu', nn.Parameter(torch.tensor(kernels_mu), requires_grad=False).view(1, 1, 1, n_kernels))
    self.register_buffer('sigma', nn.Parameter(torch.tensor(kernels_sigma), requires_grad=False).view(1, 1, 1, n_kernels))
    self.kernel_bin_weights = nn.Linear(n_kernels, 1, bias=False)
    torch.nn.init.uniform_(self.kernel_bin_weights.weight, (- 0.014), 0.014)
    self.kernel_alpha_scaler = nn.Parameter(torch.full([1, 1, n_kernels], 1, dtype=torch.float32, requires_grad=True))
    self.stop_word_reducer = nn.Linear(_embsize, 100, bias=True)
    self.stop_word_reducer2 = nn.Linear(100, 1, bias=True)
    torch.nn.init.constant_(self.stop_word_reducer2.bias, 1)
