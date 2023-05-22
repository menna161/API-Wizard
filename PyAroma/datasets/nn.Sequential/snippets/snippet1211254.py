from typing import Dict, Iterator, List
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
from allennlp.modules.text_field_embedders import TextFieldEmbedder
from allennlp.modules.matrix_attention.cosine_matrix_attention import CosineMatrixAttention


def __init__(self, word_embeddings_out_dim: int, n_grams: int, n_kernels: int, conv_out_dim: int):
    super(Conv_KNRM, self).__init__()
    self.mu = Variable(torch.cuda.FloatTensor(self.kernel_mus(n_kernels)), requires_grad=False).view(1, 1, 1, n_kernels)
    self.sigma = Variable(torch.cuda.FloatTensor(self.kernel_sigmas(n_kernels)), requires_grad=False).view(1, 1, 1, n_kernels)
    self.convolutions = []
    for i in range(1, (n_grams + 1)):
        self.convolutions.append(nn.Sequential(nn.ConstantPad1d((0, (i - 1)), 0), nn.Conv1d(kernel_size=i, in_channels=word_embeddings_out_dim, out_channels=conv_out_dim), nn.ReLU()))
    self.convolutions = nn.ModuleList(self.convolutions)
    self.cosine_module = CosineMatrixAttention()
    self.dense = nn.Linear(((n_kernels * n_grams) * n_grams), 1, bias=False)
    torch.nn.init.uniform_(self.dense.weight, (- 0.014), 0.014)
