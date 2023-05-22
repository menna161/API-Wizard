from typing import Dict, Iterator, List, Tuple
from collections import OrderedDict
import torch
import torch.nn as nn
from allennlp.nn.util import get_text_field_mask
import torch.nn.functional as F
from allennlp.modules.text_field_embedders import TextFieldEmbedder
from allennlp.modules.matrix_attention.cosine_matrix_attention import CosineMatrixAttention
from allennlp.modules.matrix_attention.dot_product_matrix_attention import DotProductMatrixAttention
from matchmaker.modules.masked_softmax import MaskedSoftmax


def __init__(self, unified_query_length: int, unified_document_length: int, max_conv_kernel_size: int, conv_output_size: int, kmax_pooling_size: int):
    super(CO_PACRR, self).__init__()
    self.cosine_module = CosineMatrixAttention()
    self.unified_query_length = unified_query_length
    self.unified_document_length = unified_document_length
    self.convolutions = []
    for i in range(2, (max_conv_kernel_size + 1)):
        self.convolutions.append(nn.Sequential(nn.ConstantPad2d((0, (i - 1), 0, (i - 1)), 0), nn.Conv2d(kernel_size=i, in_channels=1, out_channels=conv_output_size), nn.MaxPool3d(kernel_size=(conv_output_size, 1, 1))))
    self.convolutions = nn.ModuleList(self.convolutions)
    context_pool_size = 6
    self.doc_context_pool = nn.Sequential(nn.ConstantPad1d((0, (context_pool_size - 1)), 0), nn.AvgPool1d(kernel_size=context_pool_size, stride=1))
    self.masked_softmax = MaskedSoftmax()
    self.kmax_pooling_size = kmax_pooling_size
    kmax_pooling_view_percent = [0.25, 0.5, 0.75, 1]
    self.kmax_pooling_views = [int((unified_document_length * x)) for x in kmax_pooling_view_percent]
    self.dense = nn.Linear(((((len(self.kmax_pooling_views) * 2) * kmax_pooling_size) * unified_query_length) * max_conv_kernel_size), out_features=100, bias=True)
    self.dense2 = nn.Linear(100, out_features=10, bias=True)
    self.dense3 = nn.Linear(10, out_features=1, bias=False)
