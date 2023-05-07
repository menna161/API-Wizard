import torch
from torch import nn
import torchvision


def __init__(self, attention_dim, embed_dim, decoder_dim, vocab_size, encoder_dim=2048, dropout=0.5):
    "\n        :param attention_dim: size of attention network\n        :param embed_dim: embedding size\n        :param decoder_dim: size of decoder's RNN\n        :param vocab_size: size of vocabulary\n        :param encoder_dim: feature size of encoded images\n        :param dropout: dropout\n        "
    super(DecoderWithAttention, self).__init__()
    self.encoder_dim = encoder_dim
    self.attention_dim = attention_dim
    self.embed_dim = embed_dim
    self.decoder_dim = decoder_dim
    self.vocab_size = vocab_size
    self.dropout = dropout
    self.attention = Attention(encoder_dim, decoder_dim, attention_dim)
    self.embedding = nn.Embedding(vocab_size, embed_dim)
    self.dropout = nn.Dropout(p=self.dropout)
    self.decode_step = nn.LSTMCell((embed_dim + encoder_dim), decoder_dim, bias=True)
    self.init_h = nn.Linear(encoder_dim, decoder_dim)
    self.init_c = nn.Linear(encoder_dim, decoder_dim)
    self.f_beta = nn.Linear(decoder_dim, encoder_dim)
    self.sigmoid = nn.Sigmoid()
    self.fc = nn.Linear(decoder_dim, vocab_size)
    self.init_weights()
