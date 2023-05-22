import logging
import numpy as np
import torch
from fairseq.data import data_utils, FairseqDataset
from fairseq.data import BucketPadLengthDataset


def __init__(self, src, src_sizes, src_dict, tgt=None, tgt_sizes=None, tgt_dict=None, left_pad_source=True, left_pad_target=False, shuffle=True, input_feeding=True, remove_eos_from_source=False, append_eos_to_target=False, align_dataset=None, append_bos=False, eos=None, num_buckets=0):
    if (tgt_dict is not None):
        assert (src_dict.pad() == tgt_dict.pad())
        assert (src_dict.eos() == tgt_dict.eos())
        assert (src_dict.unk() == tgt_dict.unk())
    if (tgt is not None):
        assert (len(src) == len(tgt)), 'Source and target must contain the same number of examples'
    self.src = src
    self.tgt = tgt
    self.src_sizes = np.array(src_sizes)
    self.tgt_sizes = (np.array(tgt_sizes) if (tgt_sizes is not None) else None)
    self.src_dict = src_dict
    self.tgt_dict = tgt_dict
    self.left_pad_source = left_pad_source
    self.left_pad_target = left_pad_target
    self.shuffle = shuffle
    self.input_feeding = input_feeding
    self.remove_eos_from_source = remove_eos_from_source
    self.append_eos_to_target = append_eos_to_target
    self.align_dataset = align_dataset
    if (self.align_dataset is not None):
        assert (self.tgt_sizes is not None), 'Both source and target needed when alignments are provided'
    self.append_bos = append_bos
    self.eos = (eos if (eos is not None) else src_dict.eos())
    if (num_buckets > 0):
        from fairseq.data import BucketPadLengthDataset
        self.src = BucketPadLengthDataset(self.src, sizes=self.src_sizes, num_buckets=num_buckets, pad_idx=self.src_dict.pad(), left_pad=self.left_pad_source)
        self.src_sizes = self.src.sizes
        logger.info('bucketing source lengths: {}'.format(list(self.src.buckets)))
        if (self.tgt is not None):
            self.tgt = BucketPadLengthDataset(self.tgt, sizes=self.tgt_sizes, num_buckets=num_buckets, pad_idx=self.tgt_dict.pad(), left_pad=self.left_pad_target)
            self.tgt_sizes = self.tgt.sizes
            logger.info('bucketing target lengths: {}'.format(list(self.tgt.buckets)))
        num_tokens = np.vectorize(self.num_tokens, otypes=[np.long])
        self.bucketed_num_tokens = num_tokens(np.arange(len(self.src)))
        self.buckets = [(None, num_tokens) for num_tokens in np.unique(self.bucketed_num_tokens)]
    else:
        self.buckets = None
