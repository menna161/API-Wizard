from random import randint
import numpy as np
from os.path import join, dirname, abspath
import sys
import argparse
from evidence_inference.preprocess.preprocessor import SimpleInferenceVectorizer as SimpleInferenceVectorizer
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report
import torch
from torch import optim
import torch.nn as nn
from torch.nn import functional as F
from torch.autograd import Variable
from torch.nn.utils.rnn import pad_sequence
from evidence_inference.models.model_0 import InferenceNet, GRUEncoder, _get_y_vec, PaddedSequence
from evidence_inference.models.model_scan import sample_train, train_reformat, scan_reform, early_stopping
import pdb
import pdb


def __init__(self, vectorizer):
    super(ScanNet, self).__init__()
    self.vectorizer = vectorizer
    vocab_size = len(self.vectorizer.idx_to_str)
    self.out = nn.Linear(vocab_size, 1)
    self.sig = nn.Sigmoid()
