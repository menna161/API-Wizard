import torch
import torch.nn as nn
import numpy as np
import math
from torch.autograd import Variable
from EncDec import Encoder, Decoder, Attention, fix_enc_hidden, gather_last
import torch.nn.functional as F
import DAG
from Beam import Beam
import data_utils
import generate as ge
from data_utils import EOS_TOK, SOS_TOK, PAD_TOK, TUP_TOK


def __init__(self, emb_size, hsize, vocab, latents, cell_type='GRU', layers=2, bidir=True, pretrained=True, use_cuda=True, dropout=0.1):
    "\n        Args:\n            emb_size (int) : size of input word embeddings\n            hsize (int or tuple) : size of the hidden state (for one direction of encoder). If this is an integer then it is assumed\n            to be the size for the encoder, and decoder is set the same. If a Tuple, then it should contain (encoder size, dec size)\n\n            latents (LatentNode) : The root of a latent node tree (Note: Size of latent embedding dims should be 2*hsize if bidir!)\n            layers (int) : layers for encoder and decoder\n            vocab (Vocab object)\n            bidir (bool) : use bidirectional encoder?\n            cell_type (str) : 'LSTM' or 'GRU'\n            sos_idx (int) : id of the start of sentence token\n        "
    super(DAVAE, self).__init__()
    self.embd_size = emb_size
    self.vocab = vocab
    self.vocab_size = len(vocab.stoi.keys())
    self.cell_type = cell_type
    self.layers = layers
    self.bidir = bidir
    self.sos_idx = self.vocab.stoi[SOS_TOK]
    self.eos_idx = self.vocab.stoi[EOS_TOK]
    self.pad_idx = self.vocab.stoi[PAD_TOK]
    self.tup_idx = self.vocab.stoi[TUP_TOK]
    self.latent_root = latents
    self.latent_dim = self.latent_root.dim
    self.use_cuda = use_cuda
    if isinstance(hsize, tuple):
        (self.enc_hsize, self.dec_hsize) = hsize
    elif bidir:
        self.enc_hsize = hsize
        self.dec_hsize = (2 * hsize)
    else:
        self.enc_hsize = hsize
        self.dec_hsize = hsize
    in_embedding = nn.Embedding(self.vocab_size, self.embd_size, padding_idx=self.pad_idx)
    out_embedding = nn.Embedding(self.vocab_size, self.embd_size, padding_idx=self.pad_idx)
    if pretrained:
        print('Using Pretrained')
        in_embedding.weight.data = vocab.vectors
        out_embedding.weight.data = vocab.vectors
    self.encoder = Encoder(self.embd_size, self.enc_hsize, in_embedding, self.cell_type, self.layers, self.bidir, use_cuda=use_cuda)
    self.decoder = Decoder(self.embd_size, self.dec_hsize, out_embedding, self.cell_type, self.layers, attn_dim=(self.latent_dim, self.dec_hsize), use_cuda=use_cuda, dropout=dropout)
    self.logits_out = nn.Linear(self.dec_hsize, self.vocab_size)
    self.latent_in = nn.Linear(self.latent_dim, (self.layers * self.dec_hsize))
    if use_cuda:
        self.decoder = self.decoder.cuda()
        self.encoder = self.encoder.cuda()
        self.logits_out = self.logits_out.cuda()
        self.latent_in = self.latent_in.cuda()
    else:
        self.decoder = self.decoder
        self.encoder = self.encoder
        self.logits_out = self.logits_out
        self.latent_in = self.latent_in
