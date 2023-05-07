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
