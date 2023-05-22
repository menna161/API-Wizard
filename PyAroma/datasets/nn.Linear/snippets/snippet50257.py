from random import randint
import numpy as np
from os.path import join, dirname, abspath
import sys
import argparse
from evidence_inference.preprocess.preprocessor import SimpleInferenceVectorizer as SimpleInferenceVectorizer
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report
from evidence_inference.models.model_ico_scan import scan_reform
import torch
from torch import optim
import torch.nn as nn
from torch.nn import functional as F
from torch.autograd import Variable
from torch.nn.utils.rnn import pad_sequence
from evidence_inference.models.model_0 import InferenceNet, GRUEncoder, _get_y_vec, PaddedSequence
import pdb


def __init__(self, inference_vector, use_attention=False, bi_GRU=True):
    super(ScanNet, self).__init__()
    self.vectorizer = inference_vector
    init_embedding_weights = InferenceNet.init_word_vectors('embeddings/PubMed-w2v.bin', inference_vector)
    vocab_size = len(self.vectorizer.idx_to_str)
    self.use_attention = use_attention
    self.sen_encoder = GRUEncoder(vocab_size=vocab_size, use_attention=self.use_attention, hidden_size=32, embeddings=init_embedding_weights, bidirectional=bi_GRU)
    self.sen_encoder.embedding.requires_grad = False
    self.sen_encoder.embedding.weight.requires_grad = False
    self.out = nn.Linear(32, 1)
    self.sig = nn.Sigmoid()
