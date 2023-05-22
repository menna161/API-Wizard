from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import csv
import os
import logging
import argparse
import random
from tqdm import tqdm, trange
import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
from torch.utils.data.distributed import DistributedSampler
from pytorch_pretrained_bert.tokenization import BertTokenizer
from pytorch_pretrained_bert.modeling import BertForSequenceClassification
from pytorch_pretrained_bert.optimization import BertAdam
from pytorch_pretrained_bert.file_utils import PYTORCH_PRETRAINED_BERT_CACHE
from processors import InputExample, ColaProcessor, MnliProcessor, MrpcProcessor, SentimentProcessor
from apex.parallel import DistributedDataParallel as DDP
from apex.optimizers import FP16_Optimizer
from apex.optimizers import FusedAdam


def accuracy(out, labels):
    outputs = np.argmax(out, axis=1)
    return np.sum((outputs == labels))
