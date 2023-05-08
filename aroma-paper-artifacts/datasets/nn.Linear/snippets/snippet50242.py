from os.path import join, dirname, abspath
import sys
import copy
import random
import numpy as np
from scipy import stats
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
from gensim.models import KeyedVectors
import torch
from torch import optim
import torch.nn as nn
from torch.nn import functional as F
from torch.autograd import Variable
from evidence_inference.preprocess.preprocessor import SimpleInferenceVectorizer as SimpleInferenceVectorizer
from evidence_inference.models.utils import PaddedSequence
from evidence_inference.models.attention_distributions import TokenAttention, evaluate_model_attention_distribution
import pdb
import pdb
import pdb


def __init__(self, vectorizer, h_size=32, init_embeddings=None, init_wvs_path='embeddings/PubMed-w2v.bin', weight_tying=True, ICO_encoder='CBoW', article_encoder='GRU', attention_over_article_tokens=True, condition_attention=True, tokenwise_attention=False, tune_embeddings=False, h_dropout_rate=0.2):
    assert weight_tying, 'All encoders use the same embedding layer'
    if (condition_attention and (not attention_over_article_tokens)):
        raise ValueError('Must have attention in order to have conditional attention!')
    if (init_embeddings is None):
        print('loading pre-trained embeddings...')
        init_embedding_weights = InferenceNet.init_word_vectors(init_wvs_path, vectorizer)
        print('done.')
    else:
        print('Using provided embeddings')
        init_embedding_weights = init_embeddings
    if (not tune_embeddings):
        init_embedding_weights.requires_grad = False
    vocab_size = len(vectorizer.idx_to_str)
    ico_h_size = (None if (ICO_encoder is 'CBoW') else h_size)
    (i_size, i_encoder) = encoder_constructor(ICO_encoder, vocab_size, init_embedding_weights, h_size=ico_h_size)
    (c_size, c_encoder) = encoder_constructor(ICO_encoder, vocab_size, init_embedding_weights, h_size=ico_h_size)
    (o_size, o_encoder) = encoder_constructor(ICO_encoder, vocab_size, init_embedding_weights, h_size=ico_h_size)
    ICO_dims = ((i_size + c_size) + o_size)
    (a_size, article_encoder) = encoder_constructor(article_encoder, vocab_size, init_embedding_weights, h_size=h_size, query_dims=ICO_dims, use_attention=attention_over_article_tokens, condition_attention=condition_attention, tokenwise_attention=tokenwise_attention)
    self.batch_first = True
    MLP_input_size = (ICO_dims + a_size)
    cls_layer = nn.Sequential(nn.Dropout(p=h_dropout_rate), nn.Linear(MLP_input_size, 16), nn.Linear(16, 3))
    super(InferenceNet, self).__init__(vectorizer, article_encoder, i_encoder, c_encoder, o_encoder, cls_layer)
