from __future__ import absolute_import, division, print_function
import argparse
import csv
import logging
import os
import random
import sys
import numpy as np
import torch
from torch.utils.data import DataLoader, RandomSampler, SequentialSampler, TensorDataset
from torch.utils.data.distributed import DistributedSampler
from tqdm import tqdm, trange
from pytorch_pretrained_bert.file_utils import PYTORCH_PRETRAINED_BERT_CACHE
from pytorch_pretrained_bert.modeling import BertForSequenceClassification, BertConfig, WEIGHTS_NAME, CONFIG_NAME
from pytorch_pretrained_bert.tokenization import BertTokenizer
from pytorch_pretrained_bert.optimization import BertAdam, warmup_linear
import ptvsd
from apex.parallel import DistributedDataParallel as DDP
from apex.optimizers import FP16_Optimizer
from apex.optimizers import FusedAdam


def accuracy(out, labels):
    outputs = np.argmax(out, axis=1)
    return np.sum((outputs == labels))
