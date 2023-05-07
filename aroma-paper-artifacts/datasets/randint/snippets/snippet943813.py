import argparse
import os
import random
import sys
import torch
import torch.nn.functional as F
from io import StringIO
from fairseq import options, utils
from fairseq.data import Dictionary
from fairseq.data.language_pair_dataset import collate
from fairseq.models import FairseqEncoder, FairseqEncoderDecoderModel, FairseqIncrementalDecoder
from fairseq.models.fairseq_encoder import EncoderOut
from fairseq.tasks import FairseqTask
from fairseq_cli import generate, interactive, preprocess, train, validate


def create_dummy_data(data_dir, num_examples=100, maxlen=20, alignment=False):

    def _create_dummy_data(filename):
        data = torch.rand((num_examples * maxlen))
        data = (97 + torch.floor((26 * data)).int())
        with open(os.path.join(data_dir, filename), 'w') as h:
            offset = 0
            for _ in range(num_examples):
                ex_len = random.randint(1, maxlen)
                ex_str = ' '.join(map(chr, data[offset:(offset + ex_len)]))
                print(ex_str, file=h)
                offset += ex_len

    def _create_dummy_alignment_data(filename_src, filename_tgt, filename):
        with open(os.path.join(data_dir, filename_src), 'r') as src_f, open(os.path.join(data_dir, filename_tgt), 'r') as tgt_f, open(os.path.join(data_dir, filename), 'w') as h:
            for (src, tgt) in zip(src_f, tgt_f):
                src_len = len(src.split())
                tgt_len = len(tgt.split())
                avg_len = ((src_len + tgt_len) // 2)
                num_alignments = random.randint((avg_len // 2), (2 * avg_len))
                src_indices = torch.floor((torch.rand(num_alignments) * src_len)).int()
                tgt_indices = torch.floor((torch.rand(num_alignments) * tgt_len)).int()
                ex_str = ' '.join(['{}-{}'.format(src, tgt) for (src, tgt) in zip(src_indices, tgt_indices)])
                print(ex_str, file=h)
    _create_dummy_data('train.in')
    _create_dummy_data('train.out')
    _create_dummy_data('valid.in')
    _create_dummy_data('valid.out')
    _create_dummy_data('test.in')
    _create_dummy_data('test.out')
    if alignment:
        _create_dummy_alignment_data('train.in', 'train.out', 'train.align')
        _create_dummy_alignment_data('valid.in', 'valid.out', 'valid.align')
        _create_dummy_alignment_data('test.in', 'test.out', 'test.align')
