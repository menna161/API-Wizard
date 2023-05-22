import torch
import torch.nn as nn
from torch.autograd import Variable
import onqg.dataset.Constants as Constants
from onqg.models.modules.Attention import ConcatAttention
from onqg.models.modules.MaxOut import MaxOut
from onqg.models.modules.DecAssist import StackedRNN, DecInit


def __init__(self, n_vocab, ans_n_vocab, d_word_vec, d_model, n_layer, n_rnn_enc_layer, rnn, d_k, feat_vocab, d_feat_vec, d_rnn_enc_model, d_enc_model, n_enc_layer, input_feed, copy, answer, coverage, layer_attn, maxout_pool_size, dropout, device=None):
    self.name = 'rnn'
    super(RNNDecoder, self).__init__()
    self.n_layer = n_layer
    self.layer_attn = layer_attn
    self.coverage = coverage
    self.copy = copy
    self.maxout_pool_size = maxout_pool_size
    input_size = d_word_vec
    self.input_feed = input_feed
    if input_feed:
        input_size += (d_rnn_enc_model + d_enc_model)
    self.ans_emb = nn.Embedding(ans_n_vocab, d_word_vec, padding_idx=Constants.PAD)
    self.answer = answer
    tmp_in = (d_word_vec if answer else d_rnn_enc_model)
    self.decInit = DecInit(d_enc=tmp_in, d_dec=d_model, n_enc_layer=n_rnn_enc_layer)
    self.feature = (False if (not feat_vocab) else True)
    if self.feature:
        self.feat_embs = nn.ModuleList([nn.Embedding(n_f_vocab, d_feat_vec, padding_idx=Constants.PAD) for n_f_vocab in feat_vocab])
    feat_size = ((len(feat_vocab) * d_feat_vec) if self.feature else 0)
    self.d_enc_model = (d_rnn_enc_model + d_enc_model)
    self.word_emb = nn.Embedding(n_vocab, d_word_vec, padding_idx=Constants.PAD)
    self.rnn = StackedRNN(n_layer, input_size, d_model, dropout, rnn=rnn)
    self.attn = ConcatAttention((self.d_enc_model + feat_size), d_model, d_k, coverage)
    self.readout = nn.Linear(((d_word_vec + d_model) + self.d_enc_model), d_model)
    self.maxout = MaxOut(maxout_pool_size)
    if copy:
        self.copy_switch = nn.Linear((self.d_enc_model + d_model), 1)
    self.hidden_size = d_model
    self.dropout = nn.Dropout(dropout)
    self.device = device
