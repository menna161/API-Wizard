from typing import Dict, Iterator, List
import torch
import torch.nn as nn
from torch.autograd import Variable
from allennlp.modules.text_field_embedders import TextFieldEmbedder
from allennlp.modules.matrix_attention.cosine_matrix_attention import CosineMatrixAttention


def init_normal(m):
    if (type(m) == nn.Linear):
        nn.init.uniform_(m.weight, 0, 0.01)
