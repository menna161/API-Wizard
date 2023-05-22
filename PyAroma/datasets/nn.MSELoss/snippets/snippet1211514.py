from matchmaker.losses.lambdarank import LambdaLoss
from matchmaker.losses.soft_crossentropy import SoftCrossEntropy
from typing import Dict, Union
import torch
from torch import nn as nn
from transformers import AutoModel
from transformers import PreTrainedModel, PretrainedConfig


def forward(self, query: Dict[(str, torch.LongTensor)], document: Dict[(str, torch.LongTensor)], use_fp16: bool=True, output_secondary_output: bool=False, bert_part_cached: Union[(bool, torch.Tensor)]=False) -> Dict[(str, torch.Tensor)]:
    document_ids = document['input_ids'][(:, 1:)]
    if (document_ids.shape[1] > self.overlap):
        needed_padding = (self.extended_chunk_size - ((document_ids.shape[1] % self.chunk_size) - self.overlap))
    else:
        needed_padding = ((self.extended_chunk_size - self.overlap) - document_ids.shape[1])
    orig_doc_len = document_ids.shape[1]
    document_ids = nn.functional.pad(document_ids, (self.overlap, needed_padding), value=self.padding_idx)
    chunked_ids = document_ids.unfold(1, self.extended_chunk_size, self.chunk_size)
    batch_size = chunked_ids.shape[0]
    chunk_pieces = chunked_ids.shape[1]
    chunked_ids_unrolled = chunked_ids.reshape((- 1), self.extended_chunk_size)
    packed_indices = (chunked_ids_unrolled[(:, self.overlap:(- self.overlap))] != self.padding_idx).any((- 1))
    orig_packed_indices = packed_indices.clone()
    ids_packed = chunked_ids_unrolled[packed_indices]
    mask_packed = (ids_packed != self.padding_idx)
    total_chunks = chunked_ids_unrolled.shape[0]
    packed_query_ids = query['input_ids'].unsqueeze(1).expand((- 1), chunk_pieces, (- 1)).reshape((- 1), query['input_ids'].shape[1])[packed_indices]
    packed_query_mask = query['attention_mask'].unsqueeze(1).expand((- 1), chunk_pieces, (- 1)).reshape((- 1), query['attention_mask'].shape[1])[packed_indices]
    if (self.sample_n > (- 1)):
        if (self.sample_context == 'ck-small'):
            query_ctx = torch.nn.functional.normalize(self.sample_cnn3(self.sample_projector(self.bert_model.embeddings(packed_query_ids).detach()).transpose(1, 2)).transpose(1, 2), p=2, dim=(- 1))
            document_ctx = torch.nn.functional.normalize(self.sample_cnn3(self.sample_projector(self.bert_model.embeddings(ids_packed).detach()).transpose(1, 2)).transpose(1, 2), p=2, dim=(- 1))
        elif (self.sample_context == 'ck'):
            query_ctx = torch.nn.functional.normalize(self.sample_cnn3(self.bert_model.embeddings(packed_query_ids).detach().transpose(1, 2)).transpose(1, 2), p=2, dim=(- 1))
            document_ctx = torch.nn.functional.normalize(self.sample_cnn3(self.bert_model.embeddings(ids_packed).detach().transpose(1, 2)).transpose(1, 2), p=2, dim=(- 1))
        else:
            qe = self.tk_projector(self.bert_model.embeddings(packed_query_ids).detach())
            de = self.tk_projector(self.bert_model.embeddings(ids_packed).detach())
            query_ctx = self.tk_contextualizer(qe.transpose(1, 0), src_key_padding_mask=(~ packed_query_mask.bool())).transpose(1, 0)
            document_ctx = self.tk_contextualizer(de.transpose(1, 0), src_key_padding_mask=(~ mask_packed.bool())).transpose(1, 0)
            query_ctx = torch.nn.functional.normalize(query_ctx, p=2, dim=(- 1))
            document_ctx = torch.nn.functional.normalize(document_ctx, p=2, dim=(- 1))
        cosine_matrix = torch.bmm(query_ctx, document_ctx.transpose((- 1), (- 2))).unsqueeze((- 1))
        kernel_activations = (torch.exp(((- torch.pow((cosine_matrix - self.mu), 2)) / (2 * torch.pow(self.sigma, 2)))) * mask_packed.unsqueeze((- 1)).unsqueeze(1))
        kernel_res = (torch.log(torch.clamp((torch.sum(kernel_activations, 2) * self.kernel_alpha_scaler), min=0.0001)) * packed_query_mask.unsqueeze((- 1)))
        packed_patch_scores = self.sampling_binweights(torch.sum(kernel_res, 1))
        sampling_scores_per_doc = torch.zeros((total_chunks, 1), dtype=packed_patch_scores.dtype, layout=packed_patch_scores.layout, device=packed_patch_scores.device)
        sampling_scores_per_doc[packed_indices] = packed_patch_scores
        sampling_scores_per_doc = sampling_scores_per_doc.reshape(batch_size, (- 1))
        sampling_scores_per_doc_orig = sampling_scores_per_doc.clone()
        sampling_scores_per_doc[(sampling_scores_per_doc == 0)] = (- 9000)
        sampling_sorted = sampling_scores_per_doc.sort(descending=True)
        sampled_indices = (sampling_sorted.indices + torch.arange(0, (sampling_scores_per_doc.shape[0] * sampling_scores_per_doc.shape[1]), sampling_scores_per_doc.shape[1], device=sampling_scores_per_doc.device).unsqueeze((- 1)))
        sampled_indices = sampled_indices[(:, :self.sample_n)]
        sampled_indices_mask = torch.zeros_like(packed_indices).scatter(0, sampled_indices.reshape((- 1)), 1)
        if ((not self.training) and ((type(bert_part_cached) == bool) and (bert_part_cached == False))):
            packed_indices = (sampled_indices_mask * packed_indices)
            packed_query_ids = query['input_ids'].unsqueeze(1).expand((- 1), chunk_pieces, (- 1)).reshape((- 1), query['input_ids'].shape[1])[packed_indices]
            packed_query_mask = query['attention_mask'].unsqueeze(1).expand((- 1), chunk_pieces, (- 1)).reshape((- 1), query['attention_mask'].shape[1])[packed_indices]
            ids_packed = chunked_ids_unrolled[packed_indices]
            mask_packed = (ids_packed != self.padding_idx)
    with torch.set_grad_enabled(((self.sample_n == (- 1)) and self.training)):
        if (self.sample_n > (- 1)):
            self.bert_model.eval()
        if ((bert_part_cached == None) or ((type(bert_part_cached) == bool) and (bert_part_cached == False))):
            bert_vecs = self.forward_representation(torch.cat([packed_query_ids, ids_packed], dim=1), torch.cat([packed_query_mask, mask_packed], dim=1))
            packed_patch_scores = self._classification_layer(bert_vecs)
            scores_per_doc = torch.zeros((total_chunks, 1), dtype=packed_patch_scores.dtype, layout=packed_patch_scores.layout, device=packed_patch_scores.device)
            scores_per_doc[packed_indices] = packed_patch_scores
            scores_per_doc = scores_per_doc.reshape(batch_size, (- 1))
            scores_per_doc_orig = scores_per_doc.clone()
            scores_per_doc_orig_sorter = scores_per_doc.clone()
        else:
            if ((bert_part_cached.shape[0] != batch_size) or (bert_part_cached.shape[1] != chunk_pieces)):
                raise Exception(((((((('cache sanity check failed! should be:' + str(batch_size)) + ',') + str(chunk_pieces)) + ' but is: ') + str(bert_part_cached.shape[0])) + ',') + str(bert_part_cached.shape[1])))
            scores_per_doc = bert_part_cached
            scores_per_doc_orig = bert_part_cached
            scores_per_doc_orig_sorter = bert_part_cached.clone()
        if (self.sample_n > (- 1)):
            scores_per_doc = (scores_per_doc * sampled_indices_mask.view(batch_size, (- 1)))
        if (scores_per_doc.shape[1] < self.top_k_chunks):
            scores_per_doc = nn.functional.pad(scores_per_doc, (0, (self.top_k_chunks - scores_per_doc.shape[1])))
        scores_per_doc[(scores_per_doc == 0)] = (- 9000)
        scores_per_doc_orig_sorter[(scores_per_doc_orig_sorter == 0)] = (- 9000)
        score = torch.sort(scores_per_doc, descending=True, dim=(- 1)).values
        score[(score <= (- 8900))] = 0
        score = (score[(:, :self.top_k_chunks)] * self.top_k_scoring).sum(dim=1)
    if (self.sample_n == (- 1)):
        if output_secondary_output:
            return (score, {'packed_indices': orig_packed_indices.view(batch_size, (- 1)), 'bert_scores': scores_per_doc_orig})
        else:
            return score
    else:
        if output_secondary_output:
            return (score, scores_per_doc_orig, {'score': score, 'document_ids': document_ids, 'packed_indices': orig_packed_indices.view(batch_size, (- 1)), 'sampling_scores': sampling_scores_per_doc_orig, 'bert_scores': scores_per_doc_orig}, None, None)
        if (self.sample_train_type == 'mseloss'):
            return (score, scores_per_doc_orig, [[torch.nn.MSELoss()(sampling_scores_per_doc_orig, scores_per_doc_orig.detach())]], [sampling_sorted.indices, scores_per_doc_orig_sorter.sort(descending=True).indices])
        elif (self.sample_train_type == 'kldivloss'):
            return (score, scores_per_doc_orig, [[torch.nn.KLDivLoss(reduction='batchmean')(torch.softmax(sampling_scores_per_doc_orig, (- 1)), torch.softmax(scores_per_doc_orig, (- 1)).detach())]], [sampling_sorted.indices, scores_per_doc_orig_sorter.sort(descending=True).indices])
        elif (self.sample_train_type == 'crossentropy'):
            return (score, scores_per_doc_orig, [[SoftCrossEntropy()(sampling_scores_per_doc_orig, torch.softmax(scores_per_doc_orig, (- 1)).detach())]], [sampling_sorted.indices, scores_per_doc_orig_sorter.sort(descending=True).indices])
        elif (self.sample_train_type == 'lambdaloss'):
            bert_gains_indices = (torch.sort(scores_per_doc_orig_sorter, descending=True, dim=(- 1)).indices + torch.arange(0, (scores_per_doc_orig_sorter.shape[0] * scores_per_doc_orig_sorter.shape[1]), scores_per_doc_orig_sorter.shape[1], device=scores_per_doc_orig_sorter.device).unsqueeze((- 1)))
            bert_gains = torch.zeros_like(packed_indices).float()
            for i in range(self.sample_n):
                bert_gains.scatter_(0, bert_gains_indices[(:, i)].reshape((- 1)), (self.sample_n - i))
            bert_gains[(~ packed_indices)] = (- 9000)
            return (score, scores_per_doc_orig, [[LambdaLoss('ndcgLoss2_scheme')(sampling_scores_per_doc, bert_gains.view(batch_size, (- 1)).detach(), padded_value_indicator=(- 9000))]], [sampling_sorted.indices, scores_per_doc_orig_sorter.sort(descending=True).indices])
