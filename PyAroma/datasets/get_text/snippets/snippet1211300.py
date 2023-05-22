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


def forward(self, query_embeddings: torch.Tensor, document_embeddings: torch.Tensor, query_pad_oov_mask: torch.Tensor, document_pad_oov_mask: torch.Tensor, query_idfs: torch.Tensor, document_idfs: torch.Tensor, output_secondary_output: bool=False) -> torch.Tensor:
    cosine_matrix = self.cosine_module.forward(query_embeddings, document_embeddings)
    cosine_matrix = cosine_matrix[(:, None, :, :)]
    conv_results = []
    conv_results.append(torch.topk(cosine_matrix.squeeze(), k=self.kmax_pooling_size, sorted=True)[0])
    for conv in self.convolutions:
        cr = conv(cosine_matrix)
        cr_kmax_result = torch.topk(cr.squeeze(), k=self.kmax_pooling_size, sorted=True)[0]
        conv_results.append(cr_kmax_result)
    per_query_results = torch.cat(conv_results, dim=(- 1))
    weigthed_per_query = (per_query_results * self.masked_softmax(query_idfs, query_pad_oov_mask.unsqueeze((- 1))))
    all_flat = per_query_results.view(weigthed_per_query.shape[0], (- 1))
    dense_out = F.relu(self.dense(all_flat))
    dense_out = F.relu(self.dense2(dense_out))
    dense_out = self.dense3(dense_out)
    output = torch.squeeze(dense_out, 1)
    return output
