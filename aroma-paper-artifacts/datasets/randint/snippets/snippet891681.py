from __future__ import absolute_import, division, print_function, unicode_literals
import argparse
import logging
import os
import random
from io import open
import numpy as np
import torch
from torch.utils.data import DataLoader, Dataset, RandomSampler
from torch.utils.data.distributed import DistributedSampler
from tqdm import tqdm, trange
from pytorch_pretrained_bert.modeling import BertForPreTraining
from pytorch_pretrained_bert.tokenization import BertTokenizer
from pytorch_pretrained_bert.optimization import BertAdam, warmup_linear
from torch.utils.data import Dataset
import random
from apex.parallel import DistributedDataParallel as DDP
from apex.optimizers import FP16_Optimizer
from apex.optimizers import FusedAdam


def get_random_line(self):
    '\n        Get random line from another document for nextSentence task.\n        :return: str, content of one line\n        '
    for _ in range(10):
        if self.on_memory:
            rand_doc_idx = random.randint(0, (len(self.all_docs) - 1))
            rand_doc = self.all_docs[rand_doc_idx]
            line = rand_doc[random.randrange(len(rand_doc))]
        else:
            rand_index = random.randint(1, (self.corpus_lines if (self.corpus_lines < 1000) else 1000))
            for _ in range(rand_index):
                line = self.get_next_line()
        if (self.current_random_doc != self.current_doc):
            break
    return line
