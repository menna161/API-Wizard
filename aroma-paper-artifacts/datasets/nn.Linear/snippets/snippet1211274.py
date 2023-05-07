from typing import Dict, Iterator, List
import torch
import torch.nn as nn
from torch.autograd import Variable
from allennlp.modules.text_field_embedders import TextFieldEmbedder
from allennlp.modules.matrix_attention.cosine_matrix_attention import CosineMatrixAttention


def __init__(self, n_kernels: int):
    super(KNRM, self).__init__()
    self.mu = Variable(torch.cuda.FloatTensor(self.kernel_mus(n_kernels)), requires_grad=False).view(1, 1, 1, n_kernels)
    self.sigma = Variable(torch.cuda.FloatTensor(self.kernel_sigmas(n_kernels)), requires_grad=False).view(1, 1, 1, n_kernels)
    self.cosine_module = CosineMatrixAttention()
    self.dense = nn.Linear(n_kernels, 1, bias=False)
    torch.nn.init.uniform_(self.dense.weight, (- 0.014), 0.014)
