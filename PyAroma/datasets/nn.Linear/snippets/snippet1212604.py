import math
import warnings
import torch
import torch.nn as nn
from onmt.modules.util_class import Elementwise


def __init__(self, word_vec_size, word_vocab_size, word_padding_idx, position_encoding=False, feat_merge='concat', feat_vec_exponent=0.7, feat_vec_size=(- 1), feat_padding_idx=[], feat_vocab_sizes=[], dropout=0, sparse=False, fix_word_vecs=False):
    self._validate_args(feat_merge, feat_vocab_sizes, feat_vec_exponent, feat_vec_size, feat_padding_idx)
    if (feat_padding_idx is None):
        feat_padding_idx = []
    self.word_padding_idx = word_padding_idx
    self.word_vec_size = word_vec_size
    vocab_sizes = [word_vocab_size]
    emb_dims = [word_vec_size]
    pad_indices = [word_padding_idx]
    if (feat_merge == 'sum'):
        feat_dims = ([word_vec_size] * len(feat_vocab_sizes))
    elif (feat_vec_size > 0):
        feat_dims = ([feat_vec_size] * len(feat_vocab_sizes))
    else:
        feat_dims = [int((vocab ** feat_vec_exponent)) for vocab in feat_vocab_sizes]
    vocab_sizes.extend(feat_vocab_sizes)
    emb_dims.extend(feat_dims)
    pad_indices.extend(feat_padding_idx)
    emb_params = zip(vocab_sizes, emb_dims, pad_indices)
    embeddings = [nn.Embedding(vocab, dim, padding_idx=pad, sparse=sparse) for (vocab, dim, pad) in emb_params]
    emb_luts = Elementwise(feat_merge, embeddings)
    self.embedding_size = (sum(emb_dims) if (feat_merge == 'concat') else word_vec_size)
    super(Embeddings, self).__init__()
    self.make_embedding = nn.Sequential()
    self.make_embedding.add_module('emb_luts', emb_luts)
    if ((feat_merge == 'mlp') and (len(feat_vocab_sizes) > 0)):
        in_dim = sum(emb_dims)
        mlp = nn.Sequential(nn.Linear(in_dim, word_vec_size), nn.ReLU())
        self.make_embedding.add_module('mlp', mlp)
    self.position_encoding = position_encoding
    if self.position_encoding:
        pe = PositionalEncoding(dropout, self.embedding_size)
        self.make_embedding.add_module('pe', pe)
    if fix_word_vecs:
        self.word_lut.weight.requires_grad = False
