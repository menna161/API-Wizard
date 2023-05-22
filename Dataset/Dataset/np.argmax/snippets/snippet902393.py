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
from transformers import BertTokenizer, BertModel, BertForPreTraining
from transformers import AdamW, get_linear_schedule_with_warmup
from apex.parallel import DistributedDataParallel as DDP
from apex.optimizers import FP16_Optimizer
from apex.optimizers import FusedAdam


def accuracy(out, labels):
    outputs = np.argmax(out, axis=1)
    return np.sum((outputs == labels))
