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
from evidence_inference.models.model_0 import InferenceNet, CBoWEncoder, GRUEncoder, _get_y_vec, PaddedSequence
import pdb


def __init__(self, inference_vector, use_attention=False, condition_attention=False, bi_GRU=True, ICO_encoder='CBOW', h_size_ICO=32, h_size=32):
    super(ScanNet, self).__init__()
    self.vectorizer = inference_vector
    init_embedding_weights = InferenceNet.init_word_vectors('embeddings/PubMed-w2v.bin', inference_vector)
    vocab_size = len(self.vectorizer.idx_to_str)
    print('Loading Article encoder...')
    self.ICO_encoder = ICO_encoder
    self.condition_attention = condition_attention
    self.use_attention = use_attention
    print('Loading ICO encoders...')
    if (ICO_encoder == 'CBOW'):
        self.intervention_encoder = CBoWEncoder(vocab_size=vocab_size, embeddings=init_embedding_weights)
        self.comparator_encoder = CBoWEncoder(vocab_size=vocab_size, embeddings=init_embedding_weights)
        self.outcome_encoder = CBoWEncoder(vocab_size=vocab_size, embeddings=init_embedding_weights)
        self.ICO_dims = (init_embedding_weights.embedding_dim * 3)
        self.MLP_input_size = (self.ICO_dims + h_size)
    elif ((ICO_encoder == 'GRU') or (ICO_encoder == 'BIGRU')):
        self.intervention_encoder = GRUEncoder(vocab_size=vocab_size, hidden_size=h_size_ICO, embeddings=init_embedding_weights, bidirectional=(ICO_encoder == 'BIGRU'))
        self.comparator_encoder = GRUEncoder(vocab_size=vocab_size, hidden_size=h_size_ICO, embeddings=init_embedding_weights, bidirectional=(ICO_encoder == 'BIGRU'))
        self.outcome_encoder = GRUEncoder(vocab_size=vocab_size, hidden_size=h_size_ICO, embeddings=init_embedding_weights, bidirectional=(ICO_encoder == 'BIGRU'))
        self.MLP_input_size = 0
    self.sen_encoder = GRUEncoder(vocab_size=vocab_size, use_attention=self.use_attention, hidden_size=h_size, embeddings=init_embedding_weights, bidirectional=bi_GRU, condition_attention=condition_attention, query_dims=self.ICO_dims)
    for layer in (self.sen_encoder, self.intervention_encoder, self.comparator_encoder, self.outcome_encoder):
        layer.embedding.requires_grad = False
        layer.embedding.weight.requires_grad = False
    self.out = nn.Linear(self.MLP_input_size, 1)
    self.sig = nn.Sigmoid()
