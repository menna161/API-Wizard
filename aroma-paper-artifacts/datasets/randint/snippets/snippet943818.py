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
