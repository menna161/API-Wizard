import logging
import numpy as np
import torch
from fairseq.data import data_utils, FairseqDataset
from fairseq.data import BucketPadLengthDataset


def collate(samples, pad_idx, eos_idx, left_pad_source=True, left_pad_target=False, input_feeding=True):
    if (len(samples) == 0):
        return {}

    def merge(key, left_pad, move_eos_to_beginning=False):
        return data_utils.collate_tokens([s[key] for s in samples], pad_idx, eos_idx, left_pad, move_eos_to_beginning)

    def check_alignment(alignment, src_len, tgt_len):
        if ((alignment is None) or (len(alignment) == 0)):
            return False
        if ((alignment[(:, 0)].max().item() >= (src_len - 1)) or (alignment[(:, 1)].max().item() >= (tgt_len - 1))):
            logger.warning('alignment size mismatch found, skipping alignment!')
            return False
        return True

    def compute_alignment_weights(alignments):
        '\n        Given a tensor of shape [:, 2] containing the source-target indices\n        corresponding to the alignments, a weight vector containing the\n        inverse frequency of each target index is computed.\n        For e.g. if alignments = [[5, 7], [2, 3], [1, 3], [4, 2]], then\n        a tensor containing [1., 0.5, 0.5, 1] should be returned (since target\n        index 3 is repeated twice)\n        '
        align_tgt = alignments[(:, 1)]
        (_, align_tgt_i, align_tgt_c) = torch.unique(align_tgt, return_inverse=True, return_counts=True)
        align_weights = align_tgt_c[align_tgt_i[np.arange(len(align_tgt))]]
        return (1.0 / align_weights.float())
    id = torch.LongTensor([s['id'] for s in samples])
    src_tokens = merge('source', left_pad=left_pad_source)
    src_lengths = torch.LongTensor([s['source'].ne(pad_idx).long().sum() for s in samples])
    (src_lengths, sort_order) = src_lengths.sort(descending=True)
    id = id.index_select(0, sort_order)
    src_tokens = src_tokens.index_select(0, sort_order)
    prev_output_tokens = None
    target = None
    if (samples[0].get('target', None) is not None):
        target = merge('target', left_pad=left_pad_target)
        target = target.index_select(0, sort_order)
        tgt_lengths = torch.LongTensor([s['target'].ne(pad_idx).long().sum() for s in samples]).index_select(0, sort_order)
        ntokens = tgt_lengths.sum().item()
        if input_feeding:
            prev_output_tokens = merge('target', left_pad=left_pad_target, move_eos_to_beginning=True)
            prev_output_tokens = prev_output_tokens.index_select(0, sort_order)
    else:
        ntokens = src_lengths.sum().item()
    batch = {'id': id, 'nsentences': len(samples), 'ntokens': ntokens, 'net_input': {'src_tokens': src_tokens, 'src_lengths': src_lengths}, 'target': target}
    if (prev_output_tokens is not None):
        batch['net_input']['prev_output_tokens'] = prev_output_tokens
    if (samples[0].get('alignment', None) is not None):
        (bsz, tgt_sz) = batch['target'].shape
        src_sz = batch['net_input']['src_tokens'].shape[1]
        offsets = torch.zeros((len(sort_order), 2), dtype=torch.long)
        offsets[(:, 1)] += (torch.arange(len(sort_order), dtype=torch.long) * tgt_sz)
        if left_pad_source:
            offsets[(:, 0)] += (src_sz - src_lengths)
        if left_pad_target:
            offsets[(:, 1)] += (tgt_sz - tgt_lengths)
        alignments = [(alignment + offset) for (align_idx, offset, src_len, tgt_len) in zip(sort_order, offsets, src_lengths, tgt_lengths) for alignment in [samples[align_idx]['alignment'].view((- 1), 2)] if check_alignment(alignment, src_len, tgt_len)]
        if (len(alignments) > 0):
            alignments = torch.cat(alignments, dim=0)
            align_weights = compute_alignment_weights(alignments)
            batch['alignments'] = alignments
            batch['align_weights'] = align_weights
    return batch
