import torch
from torch import nn
import torch.nn.functional as F
from utils import gelu, LayerNorm
from transformer_postln import TransformerLayer, Embedding, LearnedPositionalEmbedding, SelfAttentionMask
from label_smoothing import LabelSmoothing


def __init__(self, local_rank, vocab, embed_dim, ff_embed_dim, num_heads, dropout, layers, smoothing_factor, approx):
    super(BIGLM, self).__init__()
    self.vocab = vocab
    self.embed_dim = embed_dim
    self.tok_embed = Embedding(self.vocab.size, embed_dim, self.vocab.padding_idx)
    self.pos_embed = LearnedPositionalEmbedding(embed_dim, device=local_rank)
    self.layers = nn.ModuleList()
    for i in range(layers):
        self.layers.append(TransformerLayer(embed_dim, ff_embed_dim, num_heads, dropout))
    self.emb_layer_norm = LayerNorm(embed_dim)
    self.one_more = nn.Linear(embed_dim, embed_dim)
    self.one_more_layer_norm = LayerNorm(embed_dim)
    self.out_proj = nn.Linear(embed_dim, self.vocab.size)
    self.attn_mask = SelfAttentionMask(device=local_rank)
    self.smoothing = LabelSmoothing(local_rank, self.vocab.size, self.vocab.padding_idx, smoothing_factor)
    self.dropout = dropout
    self.device = local_rank
    if (approx == 'none'):
        self.approx = None
    elif (approx == 'adaptive'):
        self.approx = nn.AdaptiveLogSoftmaxWithLoss(self.embed_dim, self.vocab.size, [10000, 20000, 200000])
    else:
        raise NotImplementedError(('%s has not been implemented' % approx))
    self.reset_parameters()
