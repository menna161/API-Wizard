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
    query_context = torch.mean(query_embeddings, dim=1)
    document_context = self.doc_context_pool(document_embeddings.transpose(1, 2)).transpose(1, 2)
    cosine_matrix_context = self.cosine_module.forward(query_context.unsqueeze(dim=1), document_context).squeeze(1)
    conv_results = []
    cr_kmax_result = [[], []]
    for view_size in self.kmax_pooling_views:
        (val, idx) = torch.topk(cosine_matrix.squeeze(dim=1)[(:, :, 0:view_size)], k=self.kmax_pooling_size, sorted=True)
        cr_kmax_result[0].append(val)
        cr_kmax_result[1].append(idx)
    cr_kmax_result[0] = torch.cat(cr_kmax_result[0], dim=(- 1))
    cr_kmax_result[1] = torch.cat(cr_kmax_result[1], dim=(- 1))
    flat_context = cosine_matrix_context.view((- 1))
    index_offset = (cr_kmax_result[1] + torch.arange(0, (cr_kmax_result[1].shape[0] * cosine_matrix_context.shape[1]), cosine_matrix_context.shape[1], device=cr_kmax_result[1].device).unsqueeze((- 1)).unsqueeze((- 1)))
    selected_context = flat_context.index_select(dim=0, index=index_offset.view((- 1))).view(cr_kmax_result[1].shape[0], cr_kmax_result[1].shape[1], (- 1))
    conv_results.append(torch.cat([cr_kmax_result[0], selected_context], dim=2))
    for conv in self.convolutions:
        cr = conv(cosine_matrix)
        cr_kmax_result = [[], []]
        for view_size in self.kmax_pooling_views:
            (val, idx) = torch.topk(cr.squeeze(dim=1)[(:, :, 0:view_size)], k=self.kmax_pooling_size, sorted=True)
            cr_kmax_result[0].append(val)
            cr_kmax_result[1].append(idx)
        cr_kmax_result[0] = torch.cat(cr_kmax_result[0], dim=(- 1))
        cr_kmax_result[1] = torch.cat(cr_kmax_result[1], dim=(- 1))
        flat_context = cosine_matrix_context.view((- 1))
        index_offset = (cr_kmax_result[1] + torch.arange(0, (cr_kmax_result[1].shape[0] * cosine_matrix_context.shape[1]), cosine_matrix_context.shape[1], device=cr_kmax_result[1].device).unsqueeze((- 1)).unsqueeze((- 1)))
        selected_context = flat_context.index_select(dim=0, index=index_offset.view((- 1))).view(cr_kmax_result[1].shape[0], cr_kmax_result[1].shape[1], (- 1))
        conv_results.append(torch.cat([cr_kmax_result[0], selected_context], dim=2))
    per_query_results = torch.cat(conv_results, dim=(- 1))
    weighted_per_query = (per_query_results * self.masked_softmax(query_idfs, query_pad_oov_mask.unsqueeze((- 1))))
    if self.training:
        weighted_per_query = weighted_per_query[(:, torch.randperm(weighted_per_query.shape[1]), :)]
    all_flat = per_query_results.view(weighted_per_query.shape[0], (- 1))
    dense_out = F.relu(self.dense(all_flat))
    dense_out = F.relu(self.dense2(dense_out))
    dense_out = self.dense3(dense_out)
    output = torch.squeeze(dense_out, 1)
    if output_secondary_output:
        return (output, {})
    return output
