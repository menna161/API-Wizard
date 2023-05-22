from typing import Dict, Iterator, List, Tuple
from collections import OrderedDict
import torch
import torch.nn as nn
from allennlp.nn.util import get_text_field_mask
import torch.nn.functional as F
from allennlp.modules.text_field_embedders import TextFieldEmbedder
from allennlp.modules.matrix_attention.cosine_matrix_attention import CosineMatrixAttention
from allennlp.modules.matrix_attention.dot_product_matrix_attention import DotProductMatrixAttention


def forward(self, query_embeddings: torch.Tensor, document_embeddings: torch.Tensor, query_pad_oov_mask: torch.Tensor, document_pad_oov_mask: torch.Tensor, output_secondary_output: bool=False) -> torch.Tensor:
    cosine_matrix = self.cosine_module.forward(query_embeddings, document_embeddings)
    cosine_matrix = cosine_matrix[(:, None, :, :)]
    conv_result = self.conv_layers(cosine_matrix)
    conv_result_flat = conv_result.view(conv_result.size(0), (- 1))
    dense_out = F.relu(self.dense(conv_result_flat))
    dense_out = F.relu(self.dense2(dense_out))
    dense_out = self.dense3(dense_out)
    output = torch.squeeze(dense_out, 1)
    if output_secondary_output:
        return (output, {})
    return output
