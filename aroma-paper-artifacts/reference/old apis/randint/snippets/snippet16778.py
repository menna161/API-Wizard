import contextlib
from io import StringIO
import os
import random
import sys
import tempfile
import unittest
import torch
from fairseq import options
import preprocess
import train
import generate
import interactive
import eval_lm
import validate


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
